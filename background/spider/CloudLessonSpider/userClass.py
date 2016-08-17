#coding:utf-8
"""
@file:      userClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-08-13 17:24
@description:
            本类用于用户信息的解析写入，大部分属于write属性
"""

class User:
    def __init__(self,author_area=None,info_dict=None,conn=None):
        self.author_area = author_area
        self.info_dict = info_dict
        if conn:
            self.conn = conn
            self.cur = self.conn.cursor()

    @property
    def username(self):
        return self.author_area.find_element_by_tag_name('a').get_attribute('title')

    @property
    def uid(self):
        return self.author_area.find_element_by_tag_name('a').get_attribute('href').split('=')[-1]

    @property
    def is_teacher(self):
        return self.author_area.find_elements_by_class_name('lector')

    @property
    def db_id(self):
        if self.info_dict:
            uid = self.info_dict['uid']
        else:
            uid = self.uid
        print('uid = ',uid)
        self.cur.execute(
                'select id from user where uid = ' + uid
            )
        data = self.cur.fetchall()
        if data:
            return data[0][0]
        else:
            return False

    def save_to_db(self):
        if self.info_dict:
            uid = self.info_dict['uid']
            username = self.info_dict['username']
            is_teacher = self.info_dict['is_teacher']
        else:
            uid = self.uid
            username = self.username
            is_teacher = self.is_teacher
        if self.db_id:
            print('this user has been saved previously')
            return False
        try:
            self.cur.execute(
                'insert into user(uid,username,is_teacher)'
                'values(%s,%s,%s)',
                (uid,username,is_teacher)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print('User:save_to_db():ERROR:'+str(e))
            return False