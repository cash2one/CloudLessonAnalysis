#coding:utf-8
"""
@file:      replyClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-08-14 3:28
@description:
            本类用于评论信息的解析写入，大部分属于write属性
"""

class Reply:
    def __init__(self,replyEle,conn=None):
        self.replyEle = replyEle
        if conn:
            self.conn = conn
            self.cur = self.conn.cursor()

    @property
    def content(self):
        return

    @property
    def content(self):
        return

    @property
    def content(self):
        return

    @property
    def content(self):
        return

    @property
    def content(self):
        return

    @property
    def content(self):
        return

    @property
    def content(self):
        return

    def save_to_db(self):
        pass