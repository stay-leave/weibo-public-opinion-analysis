# weibo-crawer
这是本科阶段的一次科研实践的代码，是基于微博信息进行舆情分析。

微博的信息爬取，主要包括微博博文、博文评论和评论所属用户的信息，有了以上数据就可以进行微博的舆情分析了。

微博博文爬取的程序我使用的是https://github.com/dataabc/weibo-search

非常感谢！

但目前对于博文评论和用户信息并没有太好的程序，为此我编写了博文评论和用户信息的爬取代码。

使用方法：

1.先爬取博文数据，得到excel文件，另存为xlsx格式。

2.使用comment crawler.py爬取博文的评论。上传了随机cookie的版本，取消了多线程，这样可以有效防止反爬（如状态码418等），程序即comments-crawler_random。

3.如果对评论数据的质量有要求，就使用data cleaning.py进行清洗。

4.使用user information crawler.py爬取评论对应的用户信息。

注：
1.所有代码都需要修改源文件的路径和爬取到的数据文件的路径。

2.爬取去年的评论需要用到特定的程序，已上传并备注，否则无法获取到日期。
    
3.需要自己添加自己的微博账号cookie。


爬取顺序是：微博正文、微博评论、用户信息。依次进行，本文解决的是后两个信息的爬取。

重要：cookie获取方式

1.登陆https://weibo.cn/

2.F12,选择网络

![image](https://user-images.githubusercontent.com/58450966/158399613-ecb09301-8937-460c-ad83-34bbc2c6f198.png)

3.重新载入，点击该文件，红圈处即是cookie

![image](https://user-images.githubusercontent.com/58450966/158399869-210f8cc3-cfd4-4394-80d9-e5cab56f9688.png)

