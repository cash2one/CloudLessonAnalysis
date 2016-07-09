#coding:utf-8
__author__ = 'lyn  <tonylu716@gmail.com>'

from background.spider.spider import LessonDataSpider

s = LessonDataSpider()

s.login(using_qq=True)