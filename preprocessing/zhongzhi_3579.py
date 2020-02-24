import cv2
import numpy as np

# 导入添加噪声的图片
img = cv2.imread(r'/media/lc/8A986A3C986A26C3/model/data/m6.png')
cv2.imshow('original', img)

# 1. cv2.medianBlur 中值滤波
# 将9个数据从小到大排列，取中间值作为当前值
median3 = cv2.medianBlur(img, 3)
cv2.imshow('median3', median3)
cv2.imwrite(r'/media/lc/8A986A3C986A26C3/model/data/m6_3.jpg', median3)

median5 = cv2.medianBlur(img, 5)
cv2.imshow('median5', median5)
cv2.imwrite(r'/media/lc/8A986A3C986A26C3/model/data/m6_5.jpg', median5)

median7 = cv2.medianBlur(img, 7)
cv2.imshow('median7', median7)
cv2.imwrite(r'/media/lc/8A986A3C986A26C3/model/data/m6_7.jpg', median7)

median9 = cv2.medianBlur(img, 9)
cv2.imshow('median9', median9)
cv2.imwrite(r'/media/lc/8A986A3C986A26C3/model/data/m6_9.jpg', median9)

cv2.waitKey(0)