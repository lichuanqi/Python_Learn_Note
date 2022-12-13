"""计算点的凸壳"""
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt


generators = np.array([[0.2, 0.2],
                       [0.2, 0.4],
                       [0.4, 0.4],
                       [0.4, 0.2],
                       [0.3, 0.6]])
hull = ConvexHull(points=generators,
                  qhull_options='QG4')

# 类的一些属性

# 输入点的坐标
print(hull.points)
# 输入尺寸>2时凸壳的表面积。输入时 points 是二维的，这是凸壳的周长。
print(hull.area)
# 输入尺寸>2时凸壳的体积。输入时 points 是二维的，这是凸壳的面积。
print(hull.volume)
# 凸壳连接线点的索引
print(hull.simplices)
# 是否能从观察点观测到
print(hull.good)