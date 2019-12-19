# ===================================
# 图像平滑操作(去噪操作)
# 1. cv2.medianBlur(进行中值滤波)
# 2. cv2.blur(均值滤波)
# 3. cv2.Guassiannblur(进行高斯滤波)
# 4. cv2.boxFilter 表示进行方框滤波
# 5. cv2.bilateralFilte 双边滤波
#    邻域直径，两个参数分别是空间高斯函数标准差，灰度值相似性高斯函数标准差


import cv2
import numpy as np

# 导入添加噪声的图片
img = cv2.imread('/media/lc/8A986A3C986A26C3/model/data/knn/300-qjys.png')
cv2.imshow('original', img)

# 1. cv2.medianBlur 中值滤波
# 将9个数据从小到大排列，取中间值作为当前值
median = cv2.medianBlur(img, 9)
cv2.imshow('median', median)
#cv2.imwrite(r'E:\model\data\300_median.jpg', median)

# 2. cv2.blur 均值滤波
# 即当对一个值进行滤波时，使用当前值与周围8个值之和，取平均做为当前值
mean = cv2.blur(img, (3, 3))
cv2.imshow('mean', mean)
#cv2.imwrite(r'E:\model\data\300_mean.jpg', mean)

# 3. cv2.GaussianBlur 高斯滤波
# 根据高斯的距离对周围的点进行加权,求平均值1，0.8， 0.6， 0.8
gaussian = cv2.GaussianBlur(img, (5, 5), 1)
cv2.imshow('gaussian', gaussian)
#cv2.imwrite(r'E:\model\data\300_gaussian.jpg', gaussian)

# 4. cv2.boxFilter 表示进行方框滤波
# box = cv2.boxFilter(img, -1, (3, 3), normalize=True)
# cv2.imshow('box', box)

# 5. cv2.bilateralFilte 双边滤波
shuangbian = cv2.bilateralFilter(img,9,75,75)
cv2.imshow('shuangbian', shuangbian)
#cv2.imwrite(r'E:\model\data\300_shuangbian.jpg', shuangbian)

cv2.waitKey(0)