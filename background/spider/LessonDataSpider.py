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

class LessonDataSpider(object):
    def __init__(self,is_visual=True,need_web=True,need_db=True,qq_login=False):
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

    def get_term_urls(self):
        urls = []
        for term_info_tuple in self.get_term_info_by_db():
            course_id = str(term_info_tuple[1])
            term_id = term_info_tuple[0]
            self.cur.execute(
                'Select url From course WHERE id = ' + course_id
            )
            course_url = self.cur.fetchall()[0][0]
            course_url = course_url.replace('/course','/learn')
            term_url = course_url + '?tid=' + term_id
            urls.append(term_url)
        return urls

    def get_term_post_pages_num(self,term_url):
        browser = self.driver
        first_page_url = term_url + '#/learn/forumindex'
        while(1):
            browser.get(first_page_url)
            if 'forumindex' in browser.current_url:
                break
            else:
                print('网页被恶意指向，重复访问',first_page_url)
                try:
                    print('存在learn页按钮，则模拟点击')
                    browser.find_element_by_xpath('//*[@id="j-startLearn"]').click()
                    time.sleep(2)
                except:
                    print('此课程该学期已停')
                    return 0
        pager_div = browser.find_element_by_xpath('//*[@id="courseLearn-inner-box"]/div/div[7]/div/div[2]/div/div[1]/div[2]')
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

    def term_is_initialized(self,term_id):
        self.cur.execute(
            'SELECT first_crawl_ok FROM term WHERE term_id = %s',term_id
        )
        return self.cur.fetchall()[0][0]

    def get_post_info_by_crawling(self,term_url,for_update=False):
        term_id = term_url.split('=')[-1]
        if (self.term_is_initialized(term_id)):
            pass
        #按发布或更新时间顺序，增量爬
        page_num = self.get_term_post_pages_num(term_url)
        browser = self.driver
        for i in range(1,page_num+1):
            print('---------------')
            print('page:',i)
            #t=2表示默认按回复数排序
            page_url = term_url + '#/learn/forumindex?t=2?p=' + str(i)
            browser.get(page_url)
            #定位帖子列表位置
            post_list = []
            while(not post_list):
                post_list = browser.find_element_by_xpath(
                    '//*[@id="courseLearn-inner-box"]/div/div[7]/div/div[2]/div/div[1]/div[1]'
                ).find_elements_by_tag_name('li')
                print('waiting for loading,search again...')
                time.sleep(1)
            for post in post_list:
                data_dict = {}
                data_dict['term_url'] = term_url
                data_dict['view_cot'] = int(post.find_element_by_class_name('watch').text.split('：')[-1])
                data_dict['reply_cot'] = int(post.find_element_by_class_name('reply').text.split('：')[-1])
                data_dict['vote_cot'] = int(post.find_element_by_class_name('vote').text.split('：')[-1])
                cnt_area = post.find_element_by_class_name('cnt')
                data_dict['teacher_joined'] = False
                if cnt_area.find_elements_by_class_name('u-forumtag'):
                    data_dict['teacher_joined'] = True
                data_dict['title'] = cnt_area.find_element_by_tag_name('a').text
                data_dict['post_id'] = cnt_area.find_element_by_tag_name('a').get_attribute('href').split('=')[-1]
                if post.find_element_by_class_name('anonyInfo').is_displayed():
                    #如果匿名发表
                    data_dict['username'] = None
                    data_dict['uid'] = None
                    data_dict['is_teacher'] = None
                else:
                    author_area = post.find_element_by_class_name('userInfo')
                    data_dict['username'] = author_area.find_element_by_tag_name('a').get_attribute('title')
                    data_dict['uid'] = author_area.find_element_by_tag_name('a').get_attribute('href').split('=')[-1]
                    data_dict['is_teacher'] = False
                    if author_area.find_elements_by_class_name('lector'):
                        data_dict['is_teacher'] = True
                time_text = post.find_element_by_tag_name('span').text
                #print(time_text)
                submit_time_string = time_text.split('|')[0].split('于')[-1][:-2]
                submit_time_list = re.split('[年月日]',submit_time_string)[:-1]
                data_dict['submit_date'] = '-'.join(submit_time_list)
                data_dict['latest_reply_date'] = time_text.split('|')[-1].split('（')[-1].split('）')[0]
                try:
                    print(data_dict['post_id'],data_dict['title'])
                except:
                    print('unicodeEncodeError')
                if not for_update:
                    self.save_post_info_to_db(data_dict)
                else:
                    self.update_post_date(data_dict)
        if page_num:
            self.cur.execute(
                'UPDATE term SET first_crawl_ok = 1 WHERE term_id = %s',term_id
            )


    def update_post_content(self):
        pass

    def update_post_date(self,data):
        self.cur.execute(
            'SELECT id FROM post WHERE post_id = %s',data['post_id']
        )
        if self.cur.fetchall():
            self.cur.execute(
                'update post set submit_date = %s,latest_reply_date = %s'
                'where post_id = %s',
                (data['submit_date'],data['latest_reply_date'],data['post_id'])
            )
            self.conn.commit()
        else:
            print('update_post_date() Error: This post had not been saved,I will execute save operation first.')
            self.save_post_info_to_db(data)

    def save_post_info_to_db(self,data):
        self.cur.execute(
            'select id from term where term_id=' + data['term_url'].split('=')[-1]
        )
        term_id = self.cur.fetchall()[0][0]
        if data['username']==None and data['uid']==None:
            #如果匿名发表，直接存post
            try:
                self.cur.execute(
                    'insert into post(post_id,term,reply_cot,vote_cot,submit_date,latest_reply_date,title,teacher_joined)'
                    'values(%s,%s,%s,%s,%s,%s,%s,%s)',
                    (data['post_id'],term_id,data['reply_cot'],data['vote_cot'],data['submit_date'],data['latest_reply_date'],data['title'],data['teacher_joined'])
                )
                self.conn.commit()
            except:
                print('this post has been saved previously')
        else:
            #实名发表
            try:
                #先存用户
                self.cur.execute(
                    'insert into user(uid,username,is_teacher)'
                    'values(%s,%s,%s)',
                    (data['uid'],data['username'],data['is_teacher'])
                )
                self.conn.commit()
            except:
                print('this user has been saved previously')
            #读取用户id
            self.cur.execute(
                'select id from user where uid=' + data['uid']
            )
            saved_user_id = self.cur.fetchall()[0][0]
            try:
                self.cur.execute(
                    'insert into post(post_id,user,term,reply_cot,vote_cot,submit_date,latest_reply_date,title,teacher_joined)'
                    'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (data['post_id'],saved_user_id,term_id,data['reply_cot'],data['vote_cot'],data['submit_date'],data['latest_reply_date'],data['title'],data['teacher_joined'])
                )
                self.conn.commit()
            except:
                print('this post has been saved previously')

    def get_post_info_by_db(self):
        pass

    def tear_down(self):
        self.driver.close()