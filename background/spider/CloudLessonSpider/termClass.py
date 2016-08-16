#coding:utf-8
"""
@file:      termClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-08-14 1:19
@description:
            对term考察主要是从数据库角度考察，而不是爬虫角度
            本类用于学期信息在db中的读取，均为read属性
"""
from courseClass import Course

class Term:
    def __init__(self,term_id=None,db_id=None,conn=None):
        if conn:
            self.conn = conn
            self.cur = conn.cursor()
        if db_id:
            self.db_id = db_id
        if term_id:
            self.term_id = term_id
            self.db_id = self.get_db_id_by_term_id()


    def get_db_id_by_term_id(self):
        self.cur.execute(
            'SELECT id FROM term WHERE term_id = %s',(self.term_id)
        )
        return self.cur.fetchall()[0][0]

    @property
    def term_id(self):
        self.cur.execute(
            'SELECT term_id FROM term WHERE id = %s',(self.db_id)
        )
        return self.cur.fetchall()[0][0]

    @property
    def url(self):
        return Course(
            db_id = self.db_course_id,
            conn = self.conn
        ).db_url.replace('/course','/learn')+'?tid='+self.term_id

    @property
    def is_initialized(self):
        self.cur.execute(
            'SELECT first_crawl_ok FROM term WHERE id = %s',(self.db_id)
        )
        return self.cur.fetchall()[0][0]

    @property
    def db_course_id(self):
        self.cur.execute(
            'select course from term where id = %s',(self.db_id)
        )
        return int(self.cur.fetchall()[0][0])

    @property
    def db_page_num(self):
        self.cur.execute(
            'select page_num from term where id = %s',(self.db_id)
        )
        return int(self.cur.fetchall()[0][0])

