"""
计算多边形的凸包
"""
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

points = [[
                116.388908,
                40.064471
            ],
            [
                116.355184,
                40.070653
            ],
            [
                116.39271,
                40.060331
            ],
            [
                116.35597,
                40.06831
            ],
            [
                116.355781,
                40.068868
            ],
            [
                116.358664,
                40.072338
            ],
            [
                116.362886,
                40.072589
            ],
            [
                116.382182,
                40.060168
            ],
            [
                116.357886,
                40.072199
            ]
        ]

# 初始化多边形并计算凸包
hull_points = Polygon(points).convex_hull
print(hull_points)

# 提取凸包的坐标
xs, ys = hull_points.exterior.coords.xy

# 展示一下
plt.figure()
plt.fill(xs, ys, alpha=0.5, label='20220801')
plt.legend()
plt.show()