# CloudLessonAnalysis
**项目介绍**：针对云课程论坛的数据爬取与分析建模，构建课程推荐系统
## 前期进行的挖掘工作
###网易云课堂
- 数据库层面，结构很清晰:四个层级，五张表，
```
Course->Term->Post->Reply, extend User
```
- 爬虫层面，围绕以上几个对象做抓取：
```
0.先针对[计算机专业]的course挖掘
1.使用selenium chrome的webdriver动态抓取
2.网易的页面比较花哨，js加载很多，元素id是动态生成的，还内嵌了不少iframe，不使用前端爬虫比较难抓数据。
4.类和方法参见lessondatespider.py
```
###SegmentFault
```
NULL
```
##云课堂数据分析
###待开发...
