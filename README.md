# CloudLessonAnalysis
**项目介绍**：针对云课程论坛的数据爬取与分析建模，构建课程推荐系统
## 前期进行的挖掘工作
###网易云课堂
- 先针对[计算机专业]课程挖掘
- 数据库层面，结构很清晰:四个层级，五张表，
```
Course->Term->Post->Reply, extend User
```
![](https://api.sinas3.com/v1/SAE_findmentor/findmentor/product_img/213132.png)
- 爬虫层面，围绕以上几个对象做抓取：
```
使用selenium chrome的webdriver动态抓取，
网易的页面比较花哨，js加载很多，元素id是动态生成的。
内嵌了不少iframe，不使用前端爬虫比较难抓数据。
类和方法参见lessondatespider.py
```
###SegmentFault
##云课堂数据分析
###待开发...
