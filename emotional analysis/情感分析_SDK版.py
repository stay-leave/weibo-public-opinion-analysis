#coding=utf-8
from aip import AipNlp
import xlrd
import re
import xlwt
import time as t
""" 
你的 APPID AK SK 
每秒钟只能调用两次
"""
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def filter_emoji(content):
	try:
	    # Wide UCS-4 build
	    cont = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')
	except re.error:
	    # Narrow UCS-2 build
	    cont = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')
	return cont.sub (u'', str(content))

def extract(inpath):
    """提取数据"""
    data = xlrd.open_workbook(inpath, encoding_override='utf-8')
    table = data.sheets()[0]#选定表
    nrows = table.nrows#获取行号
    ncols = table.ncols#获取列号
    numbers=[]
    for i in range(1, nrows):#第0行为表头
        alldata = table.row_values(i)#循环输出excel表中每一行，即所有数据
        #result_1 = alldata[1]#取出评论内容
        result_2 = alldata[2]#取出评论内容
        #result_3 = alldata[3]#取出地区
        #numbers.append([result_1,result_2,result_3])
        numbers.append(result_2)
    return numbers

def run(inpath):
    "运行程序,返回一个嵌套小列表的大列表"
    alls=[]#大列表
    all=extract(inpath)
    for i in all:#i是三个元素的小列表
        c=i[2]#日期
        b=i[1]#地区
        a=i[0]#评论内容
        a=filter_emoji(a)#表情过滤
        #a=re.sub(r'[^\u4e00-\u9fa5]','',str(a))#保证只有中文
        p = re.findall(r'回复@.*?:',a) #去除前面的无用文本
        if len(p) != 0:
            p=str(p[0])
            a=a.replace(p,'')
        else:
            pass
        if a.strip()=='':#如果a为空，就结束本次循环开始下次循环
            continue

        while True:#处理aps并发异常
            judge=client.sentimentClassify(a)#获取评论，进行情感判断
            if judge=={'error_code': 18, 'error_msg': 'Open api qps request limit reached'}:
                t.sleep(1)
                continue
            else:
                break
        if 'error_msg' in judge:#如果出现意外的报错，就结束本次循环
            continue
        print(judge)
        print(a)
        pm=judge['items'][0]['sentiment']#情感分类
        print(pm)
        pp=judge['items'][0]['positive_prob']#正向概率
        np=judge['items'][0]['negative_prob']#负向概率
        alls.append([c,b,a,pm,pp,np])
    return alls

def save_file(alls,name):
    """将一个时间段的所有评论数据保存在一个excle
    """
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.write(0,0,'评论日期')
    sheet1.write(0,1,'所属地区')
    sheet1.write(0,2,'评论内容')
    sheet1.write(0,3,'情感极性')
    sheet1.write(0,4,'正向概率')
    sheet1.write(0,5,'负向概率')
    i=1
    #for all in alls:#遍历每一页
    for data in alls:#遍历每一行
        for j in range(len(data)):#取每一单元格
            sheet1.write(i,j,data[j])#写入单元格
        i=i+1#往下一行
    #os.chdir('F:\数据爬取\参考文献')
    f.save(str(name))

if __name__ == "__main__":
    #save_file(run('数据.xls'),'情感分析.xls')
    judge=client.sentimentClassify('👏🙊')#判定为空
    print(judge)
