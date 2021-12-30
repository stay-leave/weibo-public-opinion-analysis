#coding='utf-8'
import xlrd
import xlwt
import datetime
import re
import pandas as pd
import numpy as np

data_1=pd.read_excel(r'情感负向.xlsx')
data = pd.DataFrame(data_1)#将excel文件读取并转换为dataframe格式
print(data)
data_df=data.groupby(by='日期').mean()#根据日期求均值
data_df.sort_index(ascending=True,inplace=True)#降序
data_df.drop(['uid'],axis=1,inplace=True)#删除id列
print(data_df)
data_df.to_excel('情感负向降维.xlsx')#将情感值存入excel



