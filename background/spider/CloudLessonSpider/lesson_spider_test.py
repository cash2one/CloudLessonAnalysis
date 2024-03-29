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
import time

s = LessonDataSpider(need_web=True,need_db=True ,qq_login=True)


for term_url in s.get_term_urls():
    print(term_url)
    s.get_post_info_by_crawling(
        term_url=term_url,
        for_update=False
    )
    print('---------')


'''
#测试爬取课程信息
course_list = s.get_all_cs_courses_by_crawling()
for course in course_list:
    print(course)
'''


'''
#测试写入课程信息
s.save_course_info_to_db()
'''

'''
#测试读取课程信息
course_urls = s.get_course_info_by_db()
print(course_urls)
'''

'''
term_list = s.get_term_info('http://www.icourse163.org/course/hit-1001554030')
for term in term_list:
    print(term)
'''

'''
测试爬取学期信息
for course_url in course_urls[-20:]:
    term_list = s.get_term_info(course_url)
    print('-------------')
'''

'''
测试写入学期信息
s.save_term_info_to_db()
'''

'''
测试更新课程信息
s.update_course_info()
'''