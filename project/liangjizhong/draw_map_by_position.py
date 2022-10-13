
import random
from re import T
import sys

import pandas as pd

from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts import options as opts


# 从基础信息表中读取经纬度信息
flie_path = 'D:/Cpst/项目-两集中仿真/基础表维护-20220824.xlsx'
org_data = pd.read_excel(flie_path, sheet_name='process_org')

data1 = org_data.loc[org_data['process_org_type_code'] == 1]
data2 = org_data.loc[org_data['process_org_type_code'] == 2]
data3 = org_data.loc[org_data['process_org_type_code'] == 3]
data4 = org_data.loc[org_data['process_org_type_code'] == 4]

# 构建 [名字，经度，纬度] 信息列表
nll_data = [(org_data.iloc[i]['process_org_name'], \
             org_data.iloc[i]['longitude'],        \
             org_data.iloc[i]['latitude'])       \
                 for i in range(len(org_data))]

nt_data = [[org_data.iloc[i]['process_org_name'],            \
            int(org_data.iloc[i]['process_org_type_code'])]       \
                 for i in range(len(org_data))]
print(nt_data[0:5])

# 绘制地图
geo=Geo(init_opts=opts.InitOpts(width="1200px",height='600px'))
geo.set_global_opts(title_opts=opts.TitleOpts(title='处理中心分布图',subtitle='数据来源：机构表'))
geo.add_schema(maptype='china')

# 新增点坐标
for i in range(len(nll_data)):
    geo.add_coordinate(nll_data[i][0], nll_data[i][1], nll_data[i][2])

# 新增点的属性
geo.add('处理中心', nt_data, symbol_size=4)

# 系列配置项，可配置图元样式、文字样式、标签样式、点线样式等
geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

# 自定义的每一段的范围，以及每一段的文字，以及每一段的特别的样式。例如：
pieces = [{'value': 1, 'label': '1: 省会中心局'}, \
          {'value': 2, 'label': '2: 省际集散中心'}, \
          {'value': 3, 'label': '3: 中心局'}, \
          {'value': 4, 'label': '4: 地市'}]

# 全局配置项，可配置标题、动画、坐标轴、图例等
geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces))

# 输出为html文件
geo.render('geo.html')

print('已完成')