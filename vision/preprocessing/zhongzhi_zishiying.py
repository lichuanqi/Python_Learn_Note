'''
@Description: 
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-02-24 14:40:11
'''
import cv2
import numpy as np


img = cv2.imread('/media/lc/Data/model/data/450.jpg')
# x, y, n = img.shape

# 参数设置
min_size = int(1)         # 滤波窗口的最小尺寸，一般为奇数
max_size = int(7)         # 滤波窗口的最大尺寸，一般为奇数
pading = int((max_size-1)/2) # 根据最大滤波窗口尺寸给图像添加边界

# 边界0填充,倒影填充
img_pading = cv2.copyMakeBorder(img,pading,pading,pading,pading,cv2.BORDER_DEFAULT,value=0)


cv2.imshow('add pading',img_pading)
cv2.waitKey(0)