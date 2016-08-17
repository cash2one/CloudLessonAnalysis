#coding:utf-8
"""
@file:      replyClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-08-14 3:28
@description:
            本类用于post下的reply信息的解析写入，大部分属于write属性
            进入形如/learn/ZJU-1000004001?tid=1000005000#/learn/forumdetail?pid=1000215022
            这样的post详情页面，找reply
"""
from LessonDataSpider import *
from userClass import User
from datetime import date

class Reply:
    def __init__(self,replyEle,conn=None):
        self.replyEle = replyEle
        if conn:
            self.conn = conn
            self.cur = self.conn.cursor()

    @property
    def is_anony(self):
        try:
            self.replyEle.find_element_by_class_name('userName')
            return False
        except:
            return True

    @property
    def content(self):
        return self.replyEle.find_element_by_class_name('f-richEditorText').text

    @property
    def date(self):
        date_str = self.replyEle.find_element_by_class_name('time').text
        date_info = map(lambda x:int(x),date_str.split('-'))
        return date(*date_info)

    @property
    def author(self):
        if not self.is_anony:
            return {
                'uid':self.replyEle.find_element_by_class_name('userName').get_attribute('href').split('=')[-1],
                'username':self.replyEle.find_element_by_class_name('userName').text,
                'is_teacher':0
            }
        else:
            return None

    @property
    def vote_box(self):
        return self.replyEle.find_element_by_class_name('votebox')

    @property
    def like_cot(self):
        return int(self.vote_box.find_elements_by_class_name('num')[0].text)

    @property
    def unlike_cot(self):
        try:
            return int(self.vote_box.find_elements_by_class_name('num')[1].text)
        except:
            return 0

    @property
    def comment_cot(self):
        print('cmt_btn_text = ',self.replyEle.find_element_by_class_name('cmtBtn').text)
        return int(self.replyEle.find_element_by_class_name('cmtBtn').text.split('(')[-1][:-1])

    def save_to_db(self,post_db_id):
        print(
            self.content,
            self.author,
            self.comment_cot,
            self.like_cot,
            self.unlike_cot,
            self.date
        )
        print('---------------')
        if not self.is_anony:
            author = User(info_dict=self.author,conn=self.conn)
            author.save_to_db()
            self.cur.execute(
                'insert into reply(content,create_time,author,post,comment_cot,unlike_cot,like_cot)'
                'values(%s,%s,%s,%s,%s,%s,%s)',
                (self.content,self.date,author.db_id,post_db_id,self.comment_cot,self.unlike_cot,self.like_cot)
            )
        else:
            self.cur.execute(
                'insert into reply(content,create_time,post,comment_cot,unlike_cot,like_cot)'
                'values(%s,%s,%s,%s,%s,%s)',
                (self.content,self.date,post_db_id,self.comment_cot,self.unlike_cot,self.like_cot)
            )
        self.conn.commit()



if __name__=='__main__':
    lds = LessonDataSpider(qq_login=True)
    post_ids = lds.get_post_info_by_db()
    for post_id in post_ids:
        lds.get_reply_by_crawling(post_id)
