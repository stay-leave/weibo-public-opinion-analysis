#coding='utf-8'
import xlrd
import xlwt
import datetime
import re
import pandas as pd
import numpy as np
import time

def avg(data,rate):
    #求列表的均值
    #第一个是列表，第二个是比率
    sum=0
    for i in data:
        sum=sum+i
    av=(sum/len(data))*rate
    return av
def avg_y(data):
    #求列表的均值
    #第一个是列表，第二个是比率
    sum=0
    for i in data:
        sum=sum+i
    av=sum/len(data)
    return av
def trans(date):
    """日期，必须是字符串"""
    #原算法适宜绘制地图，我的算法适宜折线图
    #算均值的算法有问题
    #尝试使用比例作为权重
    #原作者的算法：对于正向倾向文本取其正向概率，位于(0.5,1];对于负向倾向文本亦取其正向概率，位于[0,0.5)。
    #均值是将正向倾向的正向概率相加平均，负向倾向也是正向概率相加平均。
    c=[]#正向列表
    d=[]#负向列表
    e=[]#中性列表
    a=data.loc[str(date)]#选定索引为该日期的所有行
    #print(a)
    for row in a.itertuples(index=True, name='Pandas'):
        #print(getattr(row, "极性"), getattr(row, "正向概率"),getattr(row, "负向概率"))
        if getattr(row, "情感极性")=='正向':
            c.append(getattr(row, "情感值"))#正向的概率值列表
        elif getattr(row, "情感极性")=='负向':
            d.append(getattr(row, "情感值"))#负向的概率值列表
        elif getattr(row, "情感极性")=='中性':
            e.append(1)#中性列表，纯用作计数
        else:
            pass

    sum_0=len(c)+len(d)+len(e)#评论总数量
    rate_c=len(c)/sum_0#正向评论于该天占比
    rate_d=len(d)/sum_0#负向评论于该天占比
    print("正向均值："+str(rate_c))
    print("负向均值："+str(rate_d))
    nums=[date,rate_c,rate_d]
    return nums
def save_afile(all,file):
    """将降维后的数据保存在一个excel
        传递给一个列表的列表，和一个文件名
    """
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.write(0,0,'日期')
    sheet1.write(0,1,'正向比重')
    sheet1.write(0,2,'负向比重')
    i=1
    for data in all:#遍历每一行
            for j in range(len(data)):#取每一单元格
                sheet1.write(i,j,data[j])#写入单元格
            i=i+1#往下一行
    f.save(file+'.xls')
def dates(start,end):
    """生成时间序列
          输入起止日期
    """
    d=[]
    a=pd.date_range(start,end,freq='D')
    for i in a:
        i=str(i).replace('00:00:00','')
        i=i.strip()
        d.append(i)
    return d

'''
trans函数得出一天的列表，
可不做中性的情感均值
生成两年的日期，遍历
汇总并写入新的exc
'''
if __name__ == '__main__':
    data_1=pd.read_excel(r'合集_日期统一.xlsx')
    data = pd.DataFrame(data_1)#将excel文件读取并转换为dataframe格式
    print(data)
    data['日期'] = pd.to_datetime(data['日期'])
    data.set_index("日期", inplace=True)
    print(data)
    dates_0=dates('2020-12-19','2021-06-22')#日期序列生成
    #print(dates_0)
    alls=[]
    for i in dates_0:
        try:
            alls.append(trans(str(i)))
        except:
            continue
    print(alls)
    save_afile(alls,'正负向每日占比')
    print('OVER!')




