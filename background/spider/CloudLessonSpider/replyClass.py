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

class Reply:
    def __init__(self,replyEle,conn=None):
        self.replyEle = replyEle
        if conn:
            self.conn = conn
            self.cur = self.conn.cursor()

    @property
    def is_anony(self):
        return

    @property
    def content(self):
        return self.replyEle.find_element_by_class_name('f-richEditorText').text

    @property
    def date(self):
        return

    @property
    def author(self):
        return

    @property
    def vote_box(self):
        return self.replyEle.find_element_by_class_name('votebox')

    @property
    def like_cot(self):
        return

    @property
    def unlike_cot(self):
        return

    @property
    def comment_cot(self):
        return self.replyEle.find_element_by_class_name('cmtBtn').text

    def save_to_db(self):
        if self.is_anony:
            pass
        else:
            pass


if __name__=='__main__':
    lds = LessonDataSpider(qq_login=True)
    post_ids = lds.get_post_info_by_db()[:3]
    for post_id in post_ids:
        lds.get_reply_by_crawling(post_id)
