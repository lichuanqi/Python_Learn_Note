"""shapely判断点是否在多边形区域内"""

import numpy as np
from shapely import geometry


DIAOLUO =  [
        [
          1285.6141732283465,
          287.7795275590551
        ],
        [
          909.2362204724409,
          590.9291338582677
        ],
        [
          688.763779527559,
          622.4251968503937
        ],
        [
          454.90551181102364,
          595.6535433070866
        ],
        [
          283.251968503937,
          530.2992125984252
        ],
        [
          143.88188976377953,
          394.8661417322835
        ],
        [
          4.649122807017591,
          394.29824561403507
        ],
        [
          2.894736842105317,
          794.2982456140351
        ],
        [
          1285.3508771929824,
          794.2982456140351
        ]]

# 构造多边形区域
polygon_data = {'type': 'MULTIPOLYGON', 'coordinates': [[DIAOLUO]]}
polygon = geometry.shape(polygon_data)

# 虚拟一些点坐标
bbox = {'boxes': np.array([[ 0.0000000e+00,  9.5181054e-01,  1.7318889e+02,  1.7758965e+02,
         3.0490750e+02,  2.6912024e+02],
       [ 0.0000000e+00,  9.4110191e-01,  4.1009424e+02,  6.6234766e+02,
         5.5946686e+02,  8.0013013e+02],
       [ 0.0000000e+00,  9.3546057e-01,  8.7003217e+02,  2.4120624e+02,
         9.7307037e+02,  3.3350089e+02],
       [ 0.0000000e+00,  9.3209249e-01,  3.0188611e+02,  2.2183745e+02,
         3.8749222e+02,  2.8017126e+02],
       [ 0.0000000e+00,  9.2874473e-01,  1.2088418e+03,  8.2103363e+01,
         1.2771962e+03,  1.4252531e+02],
       [ 0.0000000e+00,  9.2333508e-01,  3.4392639e+02,  2.5971384e+02,
         4.6729080e+02,  3.5898624e+02],
       [ 0.0000000e+00,  9.1472417e-01,  1.0452354e+03,  1.8227104e+02,
         1.1038945e+03,  2.4082048e+02],
       [ 0.0000000e+00,  9.0431076e-01,  1.0023176e+03,  5.8217322e+02,
         1.1096108e+03,  6.8920624e+02],
       [ 0.0000000e+00,  8.9197040e-01, -1.0043986e+00,  4.9313803e+02,
         1.2916382e+02,  6.3823029e+02],
       [ 0.0000000e+00,  8.3917820e-01,  9.5743842e+02,  2.0914574e+02,
         1.0312504e+03,  2.7425458e+02]], dtype=np.float32), 'boxes_num': np.array([10])}

for box in bbox['boxes']:
    # 计算中心点
    point = geometry.Point(int((box[2]+box[4])/2), int((box[3]+box[5])/2))
    
    # 判断点是否在多边形区域内
    if polygon.intersects(point):
        print(f'{point} 在 [掉落] 监控区域内')