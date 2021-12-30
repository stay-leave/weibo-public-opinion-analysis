#coding='utf-8'
import xlrd
import re
import xlwt
import pandas as pd
def mean_0(path):
    data_1=pd.read_excel('1\\'+path+'热度.xls')
    data = pd.DataFrame(data_1)#将excel文件读取并转换为dataframe格式
    #print(data)
    data_df=data.groupby(by='主题').mean()#根据主题求均值
    data_df.sort_index(ascending=True,inplace=True)#降序
    #data_df.drop(['话题'],axis=1,inplace=True)#删除话题列
    #print(data_df)
    data_df.to_excel('2\\'+path+'热度.xlsx')#将情感值存入excel

if __name__ == "__main__":
    lis=['k_1月','k_2月','k_3月','k_4月','k_5月','k_6月','k_12月']
    for i in lis:
        mean_0(i)