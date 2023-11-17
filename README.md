CSDN，52账号：灵海之森

微信公众号：西书北影。欢迎关注
微信公众号之前没开通知，现在开了，看到会第一时间回复

环境：Python3.6

全新的微博爬虫三件套已发布，位于

https://github.com/stay-leave/weibo-crawler

基于网页端，字段和数据量更上一个台阶。

仅做学习交流使用！不收费，若发现搬运倒卖的，请私信我处理。

包含微博爬虫、LDA主题分析和情感分析三个部分。

新增话题热度、话题相似度部分。

新增地图可视化部分，数据由团队自行搜集。


1.微博爬虫

实现微博评论爬取和微博用户信息爬取，一天大概十万条。

![image](https://user-images.githubusercontent.com/58450966/147920881-f8e6f6ea-b389-417b-b13f-5d60829ecf40.png)

![image](https://user-images.githubusercontent.com/58450966/147920969-56bd4164-5599-4ecc-9918-55a42ab37b63.png)


2.LDA主题分析

实现文档主题抽取，包括数据清洗及分词、主题数的确定（主题一致性和困惑度）和最优主题模型的选择（暴力搜索）。

![image](https://user-images.githubusercontent.com/58450966/147921016-4f4bd003-4c68-4d51-82e3-eb5e14433960.png)


3.情感分析

实现评论文本的情感值计算，准确率超过97%，处于0到1之间。

![image](https://user-images.githubusercontent.com/58450966/147921147-90cd3019-a47f-496d-a783-b43d09aa1550.png)

![image](https://user-images.githubusercontent.com/58450966/147921200-db688b8e-2941-4a19-9aaa-aeabb3d9bab2.png)

4.话题热度计算

实现话题的热度的计算，同一时间内总和为1.

![image](https://user-images.githubusercontent.com/58450966/147921229-08e7ffea-c953-4efa-b52e-cdff40c615cc.png)


5.主题相似度计算

实现两个相邻时间片的话题的演化探测，以判断主题演化情况。

![image](https://user-images.githubusercontent.com/58450966/147921312-0917b2bf-d1ff-4076-933f-cb126f0fef16.png)

6.地图绘制

实现分省市情感均值、评论总数、新增确诊人数的地图可视化。

![{%F0EED5 @H@P5 1UKV~R4](https://user-images.githubusercontent.com/58450966/156149916-d1334422-3df7-416c-b9d5-317fd81323e4.png)


