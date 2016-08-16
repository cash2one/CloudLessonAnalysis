#coding:utf-8
"""
@file:      postClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-08-13 17:23
@description:
            用于post属性的解析,大部分属于write属性
"""

import re
from userClass import User
from termClass import Term

class Post:
    def __init__(self,postEle=None,post_id=None,conn=None):
        if postEle:
            self.postEle = postEle
        if conn:
            self.conn = conn
            self.cur = conn.cursor()
        if post_id:
            self.post_id = post_id
        else:
            self.post_id = self.cnt_area.find_element_by_tag_name('a').get_attribute('href').split('=')[-1]

    @property
    def is_anony(self):
        return self.postEle.find_element_by_class_name('anonyInfo').is_displayed()

    @property
    def author_area(self):
        return self.postEle.find_element_by_class_name('userInfo')

    @property
    def view_cot(self):
        return int(self.postEle.find_element_by_class_name('watch').text.split('：')[-1])

    @property
    def reply_cot(self):
        return int(self.postEle.find_element_by_class_name('reply').text.split('：')[-1])

    @property
    def vote_cot(self):
        return int(self.postEle.find_element_by_class_name('vote').text.split('：')[-1])

    @property
    def cnt_area(self):
        return self.postEle.find_element_by_class_name('cnt')

    @property
    def teacher_joined(self):
        return self.cnt_area.find_elements_by_class_name('u-forumtag')

    @property
    def title(self):
        return self.cnt_area.find_element_by_tag_name('a').text


    @property
    def submit_date(self):
        submit_time_list = re.split(
            pattern = '[年月日]',
            string = self.postEle.find_element_by_tag_name('span').text.split('|')[0].split('于')[-1][:-2]
        )[:-1]
        return '-'.join(submit_time_list)

    @property
    def latest_reply_date(self):
        return self.postEle.find_element_by_tag_name('span').text.split('|')[-1].split('（')[-1].split('）')[0]


    @property
    def url(self):
        return Term(
            db_id = self.db_term_id,
            conn = self.conn
        ).url+'#/learn/forumdetail?pid='+self.post_id

    @property
    def db_term_id(self):
        self.cur.execute(
            'select term from post where post_id = ' + self.post_id
        )
        return self.cur.fetchall()[0][0]

    @property
    def db_id(self):
        self.cur.execute(
            'select id from post where post_id = ' + self.post_id
        )
        return self.cur.fetchall()[0][0]

    def save_to_db(self):
        if self.post_id:
            print('this post has been saved previously')
            return False
        author_db_id = None
        if not self.is_anony:
            user = User(self.author_area)
            user.save_to_db()
            author_db_id = user.db_id
        try:
            self.cur.execute(
                'insert into post(post_id,user,term,reply_cot,vote_cot,view_cot,submit_date,latest_reply_date,title,teacher_joined)'
                'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (self.post_id,author_db_id,self.term_id,self.reply_cot,self.vote_cot,self.view_cot,self.submit_date,self.latest_reply_date,self.title,self.teacher_joined)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print('Post:save_to_db():ERROR:'+str(e))
            return False

    def update_info(self):
        if self.db_id:
            self.cur.execute(
                'update post set submit_date = %s,latest_reply_date = %s,view_cot = %s where post_id = %s',
                (self.submit_date,self.latest_reply_date,self.view_cot,self.post_id)
            )
            self.conn.commit()
        else:
            print('Post:update_info():ERROR: This post had not been saved,you should execute save operation first.')
            #self.save_to_db()

