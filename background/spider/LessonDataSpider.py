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
import time,pymysql,random
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
            name = self.driver.find_element_by_xpath('//*[@id="g-body"]/div/div[2]/div[1]/div/div[1]/h2').text
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


    def catch_reply(self,course_id):
        pass


    def tear_down(self):
        self.driver.close()