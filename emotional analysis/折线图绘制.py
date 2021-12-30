import pyecharts.options as opts
from pyecharts.charts import Line
import xlrd
"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://www.echartsjs.com/examples/editor.html?c=line-style

目前无法实现的功能:

暂无
"""


def file(inpath):
    """提取一个文件为一个大列表"""
    data = xlrd.open_workbook(inpath, encoding_override='utf-8')
    table = data.sheets()[0]#选定表
    nrows = table.nrows#获取行号
    ncols = table.ncols#获取列号
    numbers_1=[]
    numbers_2=[]
    for i in range(1, nrows):#第0行为表头
        alldata = table.row_values(i)#循环输出excel表中每一行，即所有数据
        numbers_1.append(alldata[0])#日期
        numbers_2.append(alldata[1])#情感值
    return numbers_1,numbers_2

x_data,y_data=file('日期降维1.1-1.19.xls')

c = (
    Line()
    .add_xaxis(x_data)
    .add_yaxis(
        "情感均值",
        y_data,
        #markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(name="自定义标记点", coord=[x[2], y[2]], value=y[2])]),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="情感均值折线图"))
    .render("情感均值折线图.html")
)