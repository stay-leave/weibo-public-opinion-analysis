#coding='utf-8'
import xlrd
import re
import xlwt

def extract_1(inpath):
    """提取数据"""
    data = xlrd.open_workbook(inpath, encoding_override='utf-8')
    table = data.sheets()[0]#选定表
    nrows = table.nrows#获取行号
    ncols = table.ncols#获取列号
    numbers=[]
    for i in range(1, nrows):#第0行为表头
        alldata = table.row_values(i)#循环输出excel表中每一行，即所有数据
        result_0 = int(alldata[2])#取出博文主题标签
        numbers.append([result_0])
    return numbers

def extract_2(inpath):
    """提取原文数据"""
    data = xlrd.open_workbook(inpath, encoding_override='utf-8')
    table = data.sheets()[0]#选定表
    nrows = table.nrows#获取行号
    ncols = table.ncols#获取列号
    numbers=[]
    for i in range(1, nrows):#第0行为表头
        alldata = table.row_values(i)#循环输出excel表中每一行，即所有数据
        result_0 = alldata[8]#取出话题
        result_1 = int(alldata[9])#取出转发
        result_2 = int(alldata[10])#取出评论
        result_3 = int(alldata[11])#取出点赞
        numbers.append([result_0,result_1,result_2,result_3])
    return numbers

def run(list_1,list_2):
    list_3=[]
    for i,j in zip(list_1,list_2):
        list_3.append(i+j)
    return list_3

def save_afile(alls,filename):
    """数据保存在一个excel"""
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.write(0,0,'主题')
    sheet1.write(0,1,'话题')
    sheet1.write(0,2,'转发')
    sheet1.write(0,3,'评论')
    sheet1.write(0,4,'点赞')
    i=1
    for data in alls:#遍历每一行
        for j in range(len(data)):#取第一个元素的每一单元格
            sheet1.write(i,j,data[j])#写入单元格
        i=i+1#往下一行
    f.save(filename)

if __name__ == "__main__":
    lis=['k_1月','k_2月','k_3月','k_4月','k_5月','k_6月','k_12月']
    for i in lis:
        list_1=extract_1(r'正式流程及文件\3.数据分析\主题分析\推文话题标签\\'+i+'.xlsx')
        list_2=extract_2(r'正式流程及文件\2.数据处理\正文信息\excel分月\\'+i+'.xlsx')
        save_afile(run(list_1,list_2),'1\\'+i+'热度.xls')