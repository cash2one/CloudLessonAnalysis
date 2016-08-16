# CloudLessonAnalysis
**项目介绍**：针对云课程论坛的数据爬取与分析建模，构建课程推荐系统
## 前期进行的挖掘工作
###网易云课堂
- 先针对[计算机专业]课程挖掘
- 数据库层面，结构很清晰:四个层级，五张表，
```
Course->Term->Post->Reply, extend User
```
![](https://api.sinas3.com/v1/SAE_visualspider/visualspider/123.png)
- 爬虫层面，围绕这几个对象做爬取
```
参见lessondatespider.py
```
###SegmentFault
##云课堂数据分析
###待开发...
