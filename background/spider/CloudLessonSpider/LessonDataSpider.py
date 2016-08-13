#coding:utf-8
"""
@file:      LessonDataSpider.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-07-08 12:28
@description:
            爬取网易云课堂的数据
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,pymysql,random,re
from threading import Thread
from postClass import Post
from termClass import Term
from replyClass import Reply

class LessonDataSpider(object):
    def __init__(
            self,is_visual=True,    need_web=True,
            need_db=True,           qq_login=False
    ):
        if qq_login:
            need_web = True
        if need_web:
            if is_visual:
                self.driver = webdriver.Chrome()
            else:
                self.driver = webdriver.PhantomJS()
        if need_db:
            self.conn = pymysql.connect(
                host='localhost',   port=3306,
                user='root',        passwd='',
                db='cloudlesson',   charset='utf8'
            )
            self.cur = self.conn.cursor()
        if qq_login:
            self.login(using_qq=True)


    def login(self,email=None,passwd=None,using_qq=False):
        #使用qq登陆，可避开验证码认证
        if not using_qq:
            if email==None or passwd==None:
                raise Exception('If you do not want to login via qq, please fill in email and password!')
        browser = self.driver
        while(1):
            try:
                browser.get('http://study.163.com/member/login.htm')
                if WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.ID,'j-ursContainer'))
                ):
                    break
            except:
                print('网页加载异常,重复访问...')
        if not using_qq:
            browser.switch_to_frame('x-URS-iframe')
            email_input = browser.find_element_by_name('email')
            passwd_input = browser.find_element_by_name('password')
            email_input.send_keys(email)
            passwd_input.send_keys(passwd)
            browser.find_element_by_xpath('//*[@id="dologin"]').click()
            time.sleep(3)
            if not browser.find_element_by_xpath('//*[@id="dologin"]'):
                print('使用邮箱:{} 登陆成功'.format(email))
            else:
                print('检查邮箱或密码，若出现验证码请使用qq登陆')
        else:
            browser.find_element_by_class_name('socialBox').find_element_by_class_name('itm2').click()
            browser.switch_to_frame('ptlogin_iframe')
            while(1):
                try:
                    qq = WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.XPATH,'//*[@id="qlogin_list"]/a'))
                    )
                    if qq:
                        qq_id = qq.get_attribute('uin')
                        qq.click()
                        print('检测到qq,使用qq: {} 登陆成功'.format(qq_id))
                        break
                except:
                    print('请登录一个qq,页面刷新...')
                    browser.refresh()
                    browser.switch_to_frame('ptlogin_iframe')
        time.sleep(2)


    def get_all_cs_courses_by_crawling(self):
        data_list = []
        browser = self.driver
        browser.get('http://study.163.com/curricula/cs.htm')
        course_lists = browser.find_elements_by_class_name('list')
        for course_list in course_lists:
            a_ele_list = course_list.find_elements_by_tag_name('a')
            for a_ele in a_ele_list:
                course_url = a_ele.get_attribute('href')
                course_id = course_url.split('/')[-1]
                data_list.append((course_url,course_id))
        return data_list


    def save_course_info_to_db(self):
        for course_tuple in self.get_all_cs_courses_by_crawling():
            self.cur.execute(
                'insert into course(url,course_id)'
                'values (%s,%s)',
                course_tuple
            )
            self.conn.commit()


    def update_course_info(self):
        for course in self.get_course_info_by_db():
            url = course[0]
            id = course[1]
            self.driver.get(url)
            name = self.driver.find_element_by_xpath(
                '//*[@id="g-body"]/div/div[2]/div[1]/div/div[1]/h2'
            ).text
            print(name)
            self.cur.execute(
                'update course set name=%s'
                'where id=%s',
                (name,id)
            )
            self.conn.commit()


    def get_course_info_by_db(self):
        self.cur.execute(
            'select url,id from course'
        )
        return self.cur.fetchall()


    def get_term_info_by_crawling(self,course_url):
        browser = self.driver
        cot = 0
        launched_by_select = False
        term_data_list = []
        while(1):
            if not launched_by_select:
                browser.get(course_url)
            try:
                u_select = browser.find_element_by_class_name('u-select')
                #print('有多学期选项')
                u_select.click()
                terms = u_select.find_elements_by_class_name('list')
                terms[cot].click()
                url = browser.current_url
                term_id = url.split('/')[-2].split('?')[1].split('=')[-1][:-1]
                term_data_list.append((url,term_id))
                if terms[cot] != terms[-1]:
                    cot += 1
                    launched_by_select=True
                else:
                    break
            except:
                #print('无多学期选项')
                try:
                    #新版本云课堂http://study.163.com/
                    j_button = browser.find_element_by_class_name('j-button')
                except:
                    try:
                        #老版本慕课http://www.icourse163.org/
                        j_button = browser.find_element_by_class_name('m-btnList')
                    except:
                        break
                try:
                    url = j_button.find_element_by_tag_name('a').get_attribute('href')
                except:
                    #a标签url都没有，表示没有学期信息，直接跳出循环
                    break
                if url:
                    #print('url可见，直接获取')
                    term_id = url.split('=')[-1]
                else:
                    #print('url不可见，打开后查看')
                    #有可能是尚未开课，未参加课程，或者就是不可见
                    j_button.click()
                    url = browser.current_url
                    if(len(url.split('='))==1):
                        #print('尚未开课')
                        break
                    else:
                        #开课后的都有tid
                        term_id = url.split('=')[-1].split('#')[0]
                term_data_list.append((url,term_id))
                break
        #print('\n')
        return term_data_list


    def save_term_info_to_db(self):
        course_tuples = self.get_course_info_by_db()
        for course_tuple in course_tuples:
            course_id = course_tuple[1]
            course_url = course_tuple[0]
            term_info_list = self.get_term_info_by_crawling(course_url)
            for term_info in term_info_list:
                print((term_info[1],course_id))
                self.cur.execute(
                    'insert into term(term_id,course)'
                    'values (%s,%s)',
                    (term_info[1],course_id)
                )
                self.conn.commit()


    def get_term_info_by_db(self):
        self.cur.execute(
            'select term_id,course from term'
        )
        return self.cur.fetchall()


    def get_term_url(self,post_id=None,term_id=None,course_id=None):
        if term_id==None and post_id==None:
            raise Exception('I cannot locate the term without term_id or post_id.')
        if term_id:
            return Term(term_id).url
        else:
            return Term(
                db_id = Post(post_id=post_id).db_term_id
            ).url


    def get_term_urls(self):
        urls = []
        for term_info_tuple in self.get_term_info_by_db():
            term_id = term_info_tuple[0]
            term_url = self.get_term_url(term_id=term_id)
            urls.append(term_url)
        return urls


    def get_term_post_pages_num(self,term_url,from_db=False):
        term_id = term_url.split('=')[-1]
        if from_db:
            return Term(term_id=term_id).db_page_num
        browser = self.driver
        first_page_url = term_url + '#/learn/forumindex'
        while(1):
            browser.get(first_page_url)
            if 'forumindex' in browser.current_url:
                break
            else:
                print('网页被重定向')
                try:
                    print('存在learn页按钮，模拟点击')
                    browser.find_element_by_xpath('//*[@id="j-startLearn"]').click()
                    time.sleep(2)
                except:
                    print('此课程该学期已停')
                    return 0
        pager_div = browser.find_element_by_xpath(
            '//*[@id="courseLearn-inner-box"]/div/div[7]/div/div[2]/div/div[1]/div[2]'
        )
        if not pager_div.is_displayed():
            return 1
        a_list = browser.find_element_by_xpath(
            '//*[@id="courseLearn-inner-box"]/div/div[7]/div/div[2]/div/div[1]/div[2]'
        ).find_elements_by_tag_name('a')
        last_page_a = None
        for a in a_list:
            if a.is_displayed() and a.text!='下一页':
                last_page_a = a
            else:
                break
        num = last_page_a.text
        return int(num)


    def crawl_page_posts_data(
        self,   term_url,   page_index,   for_update=False,   crawl_delta=True
    ):
        browser = self.driver
        print('---------------')
        #t=2表示默认按回复数排序,t=0是按最新发布排序
        if crawl_delta:
            order = '0'
        else:
            order = '2'
        page_url = term_url + '#/learn/forumindex?t='+ order +'?p=' + str(page_index)
        browser.get(page_url)
        #定位帖子列表位置
        post_list = []
        while(not post_list):
            post_list = browser.find_element_by_xpath(
                '//*[@id="courseLearn-inner-box"]/div/div[7]/div/div[2]/div/div[1]/div[1]'
            ).find_elements_by_tag_name('li')
            print('waiting for loading,search again...')
            time.sleep(1)
        for postEle in post_list:
            if for_update:
                Post(postEle).update_info()
            else:
                Post(postEle).save_to_db()


    def get_post_info_by_crawling(self,term_url,for_update=False):
        term_id = term_url.split('=')[-1]
        current_page_num = self.get_term_post_pages_num(term_url,from_db=False)
        saved_page_num = self.get_term_post_pages_num(term_url,from_db=True)
        print((current_page_num,saved_page_num))
        if current_page_num==0:
            return
        if Term(term_id=term_id).is_initialized:
            print('current_page_num:{},saved_page_num:{}'.format(current_page_num,saved_page_num))
            if current_page_num > saved_page_num or current_page_num < saved_page_num:
                self.cur.execute(
                    'update term set page_num = %s where term_id= %s',(current_page_num,term_id)
                )
                self.conn.commit()
            #按发布或更新时间顺序，爬增量
            if current_page_num >= saved_page_num:
                for i in range(1,current_page_num-saved_page_num+2):
                    print('page:{}/{}'.format(i,current_page_num-saved_page_num+1))
                    self.crawl_page_posts_data(
                        term_url=term_url,      page_index=i,
                        for_update=for_update,  crawl_delta=True
                    )
            else:
                print('current < saved, kidding me???')
        else:
            #第一次初始化数据时全部页都爬取保存
            for i in range(1,current_page_num+1):
                print('page:{}/{}'.format(i,current_page_num))
                self.crawl_page_posts_data(
                    term_url=term_url,      page_index=i,
                    for_update=for_update,  crawl_delta=False
                )
            if current_page_num:
                self.cur.execute("UPDATE term SET first_crawl_ok = 1 WHERE term_id = %s",term_id)


    def update_post_content(self,post_id,browser_set_ok=False):
        if not browser_set_ok:
            post_url = self.get_post_url(post_id)
            self.driver.get(post_url)
        cnt = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="courseLearn-inner-box"]/div/div[2]/div/div[1]/div/div[2]'))
        ).text
        #print(content)
        self.cur.execute(
            'update post set content="{}" where post_id = {}'.format(cnt,post_id)
        )
        self.conn.commit()


    def get_post_info_by_db(self):
        pass


    def get_reply_by_crawling(self,post_id):
        browser = self.driver
        browser.get(Post(post_id=post_id).url)
        self.update_post_content(post_id=post_id,browser_set_ok=True)
        reply_list = browser.find_element_by_xpath(
            '//*[@id="courseLearn-inner-box"]/div/div[2]/div/div[4]/div/div[1]/div[1]'
        ).find_elements_by_class_name('f-pr')
        for replyEle in reply_list:
            Reply(replyEle).save_to_db()


    def tear_down(self):
        self.driver.close()