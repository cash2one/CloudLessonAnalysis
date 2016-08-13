#coding:utf-8
"""
@file:      courseClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-08-14 2:10
@description:
            本类用于课程信息在db中的读取，均read属性
"""

class Course:
    def __init__(self,db_id,conn=None):
        self.db_id = db_id
        if conn:
            self.conn = conn
            self.cur = conn.cursor()

    @property
    def db_url(self):
        self.cur.execute(
            'select url from course where id = ' + self.db_id
        )
        return self.cur.fetchall()[0][0]

    @property
    def db_course_id(self):
        self.cur.execute(
            'select course_id from course where id = ' + self.db_id
        )
        return self.cur.fetchall()[0][0]