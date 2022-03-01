from pyecharts import options as opts
from pyecharts.charts import Map


data = [('北京',21714),('天津',2984),('河北',3925),('山西',1791),('内蒙古',1157),('辽宁',4459),('吉林',1463),('黑龙江',2282),
        ('上海',12183),('江苏',10398),('浙江',9049),('安徽',3703),('福建',4525),('江西',1932),('山东',6845),('河南',4340),
        ('湖北',5484),('湖南',3208),('广东',24903),('广西',2650),('海南',1127),('重庆',3126),('四川',7515),('贵州',931),
        ('云南',1680),('西藏',411),('陕西',3073),('甘肃',693),('青海',223),('新疆',1032),('台湾',397),
        ('宁夏',355),('澳门',459),('香港',1206),('南海诸岛',1127)]
def map_china() -> Map:
  c = (
      Map(init_opts=opts.InitOpts(width='720px', height='720px'))
    .add(series_name="评论数/条", data_pair=data, maptype="china",zoom = 1,center=[105,38])
    .set_global_opts(
      title_opts=opts.TitleOpts(title=""),
      visualmap_opts=opts.VisualMapOpts(max_=9999,is_piecewise=True,
              pieces=[{"max": 199, "min": 0, "label": "0-199","color":"#F5F5DC"},
                  {"max": 499, "min": 200, "label": "200-499", "color": "#F5DEB3"},
                  {"max": 999, "min": 500, "label": "500-999", "color": "#F4A460"},
                  {"max": 4999, "min": 1000, "label": "1000-4999","color":"#EE7942"},
                  {"max": 9999, "min": 5000, "label": "5000-9999", "color":"#D2691E"},
                  {"max": 19999, "min": 10000, "label": "10000-19999","color":"#B22222"},
                  {"max": 25000, "min": 20000,"label": ">=20000","color":"#8B2323"}]
                       )
    )
  )
  return c

d_map = map_china()
d_map.render("地图降维-求和.html")