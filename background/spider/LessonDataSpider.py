#coding:utf-8
__author__ = 'lyn  <tonylu716@gmail.com>'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time,pymysql,random
from threading import Thread

class LessonDataSpider(object):
    def __init__(self,is_visual=True):
        if is_visual:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.PhantomJS()


    def login(self,email=None,passwd=None,using_qq=False):
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
            print('使用邮箱:{} 登陆成功'.format(email))
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


    def catch_reply(self):
        pass


    def save_to_db(self):
        pass


    def tear_down(self):
        self.driver.close()