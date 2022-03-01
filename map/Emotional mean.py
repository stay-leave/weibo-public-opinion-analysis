from pyecharts import options as opts
from pyecharts.charts import Map


data = [('北京',0.6901),('天津',0.6922),('河北',0.684),
        ('山西',0.6844),('内蒙古',0.6969),('辽宁',0.6969),
        ('吉林',0.6928),('黑龙江',0.6857),
        ('上海',0.6918),('江苏',0.69),
        ('浙江',0.6938),('安徽',0.7035),('福建',0.6856),
        ('江西',0.7105),('山东',0.7014),('河南',0.7093),
        ('湖北',0.6956),('湖南',0.7015),('广东',0.6915),
        ('广西',0.6902),('海南',0.6982),('重庆',0.7081),
        ('四川',0.7066),('贵州',0.7019),
        ('云南',0.7010),('西藏',0.708),
        ('陕西',0.6904),('甘肃',0.6948),('青海',0.7245),
        ('新疆',0.7061),('台湾',0.6782),
        ('宁夏',0.686),('澳门',0.6708),('香港',0.6818),('南海诸岛',0.6982)]
def map_china() -> Map:
  c = (
    Map(init_opts=opts.InitOpts(width='720px', height='720px'))
    .add(series_name="情感均值", data_pair=data, maptype="china",zoom = 1,center=[105,38])
    .set_global_opts(
      title_opts=opts.TitleOpts(title=""),
      visualmap_opts=opts.VisualMapOpts(max_=9999,is_piecewise=True,
              pieces=[
                  {"max": 0.68, "min": 0.67, "label": "0.67-0.68", "color": "#F5F5DC"},
                  {"max": 0.69, "min": 0.68, "label": "0.68-0.67", "color": "#F5DEB3"},
                  {"max": 0.70, "min": 0.69, "label": "0.69-0.70","color":"#F4A460"},
                  {"max": 0.71, "min": 0.70, "label": "0.70-0.71", "color":"#D2691E"},
                  {"max": 0.72, "min": 0.71, "label": "0.71-0.72","color":"#B22222"},
                  {"max": 0.73, "min": 0.72, "label": "0.72-0.73","color":"#8B2323"}]
                       )
    )
  )
  return c

d_map = map_china()
d_map.render("地图情感均值.html")