import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
from pyecharts import options as opts
from pyecharts.charts import Map


mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

data = pd.read_excel('新增.xlsx')

f= data["省份"]
a= data["2020年12月9日累计确诊数"]
b= data["2021年6月22日累计确诊数"]
c= data["新增确诊"]
k=[list(z) for z in zip(f, c)]

def map_china() -> Map:
  c = (
    Map(init_opts=opts.InitOpts(width='720px', height='720px'))
    .add(series_name="新增确诊人数/人", data_pair=k, maptype="china",zoom = 1,center=[105,38])
    .set_global_opts(
      title_opts=opts.TitleOpts(title=""),
      visualmap_opts=opts.VisualMapOpts(max_=9999,is_piecewise=True,
              pieces=[{"max": 100, "min": 0, "label": "<100","color":"#F5F5DC"},
                  {"max": 500, "min": 100, "label": "100-499", "color": "#F5DEB3"},
                  {"max": 999, "min": 500, "label": "500-999", "color": "#F4A460"},
                  {"max": 2000, "min": 1000, "label": "1000-1999","color":"#EE7942"},
                  {"max": 5000, "min": 2000, "label": "2000-4999", "color":"#D2691E"},
                  {"max": 10000, "min": 5000, "label": "5000-10000","color":"#B22222"},
                  {"max": 15000, "min":10000, "label": ">10000","color":"#8B2323"}])
    )
  )
  return c

d_map = map_china()
d_map.render("新增确诊人数.html")