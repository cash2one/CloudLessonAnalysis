#coding:utf-8
"""
@file:      lesson_spider_test.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-07-09 12:28
@description:
            test lesson data spider
"""

from background.spider.LessonDataSpider import LessonDataSpider

s = LessonDataSpider()

s.login(using_qq=True)