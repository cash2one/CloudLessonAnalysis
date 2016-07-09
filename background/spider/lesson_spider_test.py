#coding:utf-8
__author__ = 'lyn  <tonylu716@gmail.com>'

from background.spider.LessonDataSpider import LessonDataSpider

s = LessonDataSpider()

s.login(using_qq=True)