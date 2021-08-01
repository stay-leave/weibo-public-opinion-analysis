#coding='utf-8'
import xlrd
import re
import requests
import xlwt
import os
import time as t
import random
import numpy as np	
import datetime
import urllib3
from multiprocessing.dummy import Pool as ThreadPool

urllib3.disable_warnings()
cookie=''#微博的cookie

headers = {
				  'Accept-Encoding': 'gzip, deflate, sdch',
				 'Accept-Language': 'en-US,en;q=0.8',
				 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				 'Referer': 'https://www.baidu.com/',
			    'Connection': 'keep-alive',
				'Cookie': cookie,
				}

def require(url):
	"""获取网页源码"""
	while True:
		try:
			response = requests.get(url, headers=headers,timeout=(30,50),verify=False)
			#print(url)
			code_1=response.status_code
			#print(type(code_1))
			#t.sleep(random.randint(1,2))
			if code_1==200:
				print('正常爬取中，状态码：'+str(code_1))#状态码
				t.sleep(random.randint(1,2))
				break
			else:
				print('请求异常，重试中，状态码为：'+str(code_1))#状态码
				t.sleep(random.randint(2,3))
				continue
		except:
			t.sleep(random.randint(2,3))
			continue

	#print(response.encoding)#首选编码
	#response.encoding=response.apparent_encoding
	html=response.text#源代码文本
	return html

def html_1(url):#返回网页源码和评论页数
	html=require(url)
	try:
		page=re.findall('&nbsp;1/(.*?)页',html,re.S)
		page=int(page[0])
	except:
		page=0
	#page=re.findall('<input name="mp" type="hidden" value="(.*?)">',html,re.S)
	return html,page

def count(alls):
	n=0
	for all in alls:
		for i in all:
			n=n+1
	return n


def body(h_1):#主体
	html_2=re.findall('<div class="c" id="C.*?">(.*?)</div>',str(h_1),re.S)
	html_2=str(html_2)
	
	user_ids=re.findall('<a href=".*?&amp;fuid=(.*?)&amp;.*?">举报</a> ',html_2,re.S)#从举报链接入手
	
	names_0=re.findall('<a href=.*?>(.*?)</a>',html_2,re.S)
	names=[]#用户名
	ma=[ '举报', '赞[]', '回复']
	pattern = re.compile(r'\d+')#匹配数字
	for i in names_0:
		i=re.sub(pattern, "", i)
		if i not in ma:
			if '@' not in i:
				names.append(i)

	pattern_0= re.compile(r'回复<a href=.*?</a>:')#匹配回复前缀
	pattern_0_1= re.compile(r'<a href=.*?</a>')#匹配回复内容后面的表情图片地址
	pattern_0_2= re.compile(r'<img alt=.*?/>')#匹配回复内容的图片地址
	contents=[]#评论内容
	contents_2=[]#评论内容初步
	contents_0=re.findall('<span class="ctt">(.*?)</span>',html_2,re.S)#一级
	contents_1=re.findall('<a href=.*?>@.*?</a>(.*?)<a href=.*?>举报</a> ',html_2,re.S)#二级

	for i in contents_0:
		i=re.sub(pattern_0,'',i)
		i=re.sub(pattern_0_1,'',i)
		i=re.sub(pattern_0_2,'',i)
		i=i.replace(':','')
		i=i.strip()
		contents_2.append(i)

	for i in contents_1:
		i=re.sub(pattern_0,'',i)
		i=re.sub(pattern_0_1,'',i)
		i=re.sub(pattern_0_2,'',i)
		i=i.replace('</span>','')
		i=i.replace('&nbsp;','')
		i=i.replace(':','')
		i=i.strip()
		contents_2.append(i)

	for i in contents_2:
		i=re.sub('\s','',i)#去除空白
		if len(i)==0:
			pass
		else:
			contents.append(i)
	times_0=re.findall('<span class="ct">(.*?)</span>',html_2,re.S)
	times=[]#时间
	pattern_1= re.compile(r'\d{2}月\d{2}日')#匹配日期
	for i in times_0:
		try:
			t_1= re.match(pattern_1, i).group()
		except:
			a=datetime.datetime.now().strftime('%m%d')
			t_1=a[:2]+'月'+a[2:]+'日'#改为当天
		times.append(t_1)
	
	all=[]
	for i in range(len(user_ids)):
		try:
			al=[user_ids[i],names[i],contents[i],times[i]]
		except:
			j='空'
			contents.append(j)
			al=[user_ids[i],names[i],contents[i],times[i]]
		all.append(al)
	return all

def save_afile(alls,filename):
    """将数据保存在一个excel"""
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.write(0,0,'用户ID')
    sheet1.write(0,1,'用户名')
    sheet1.write(0,2,'评论内容')
    sheet1.write(0,3,'时间')
    i=1
    for all in alls:
        for data in all:
            for j in range(len(data)):
                sheet1.write(i,j,data[j])
            i=i+1
    f.save(r'今年/'+filename+'.xls')#保存路径

def extract(inpath,l):
    """取出一列数据"""
    data = xlrd.open_workbook(inpath, encoding_override='utf-8')
    table = data.sheets()[0]#选定表
    nrows = table.nrows#获取行号
    ncols = table.ncols#获取列号
    numbers=[]
    for i in range(1, nrows):#第0行为表头
        alldata = table.row_values(i)#循环输出excel表中每一行，即所有数据
        result = alldata[l]#取出表中第一列数据
        numbers.append(result)
    return numbers

def run(ids):
	b=ids[0]#bid
	u=str(ids[1]).replace('.0','')#uid
	alls=[]#每次循环就清空一次
	pa=[]#空列表判定
	url='https://weibo.cn/comment/'+str(b)+'?uid='+str(u)#一个微博的评论首页
	html,page=html_1(url)
	#print(url)
	if page==0:#如果为0，即只有一页数据
		#print('进入页数为0')
		try:
			data_1=body(html)
		except:
			data_1=pa
		alls.append(data_1)#将首页爬取出来
		#print('共计1页,共有'+str(count(alls))+'个数据')
	else:#两页及以上
		#print('进入两页及以上')
		#print('页数为'+str(page))
		for j in range(1,page+1):#从1到page
			if j>=51:
				break
			else:
				url_1=url+'&rl=1'+'&page='+str(j)
				#print(url_1)
				htmls,pages=html_1(url_1)
				alls.append(body(htmls))
			t.sleep(1)
	print('共计'+str(page)+'页,共有'+str(count(alls))+'个数据')
	save_afile(alls,b)

	print('微博号为'+str(b)+'的评论数据文件、保存完毕')

if __name__ == '__main__':
	#由于微博限制，只能爬取前五十页的
	#里面的文件是爬取到的正文文件
	bid=extract('正文_2.xlsx',1)#1是bid，2是u_id
	uid=extract('正文_2.xlsx',2)

	ids=[]#将bid和uid匹配并以嵌套列表形式加入ids
	for i,j in zip(bid,uid):
		ids.append([i,j])
	#多线程
	pool = ThreadPool()
	pool.map(run, ids)
		
		


