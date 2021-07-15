'''
@Description: 灰度图像二值化的几种方法
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-02-23 18:23:45
'''
import cv2
import numpy as np

# 读取一张铁路场景的图片
imgpath = '/media/lc/Data/modle_and_code/data/m4.png'
img = cv2.imread(imgpath)

img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

cv2.imshow('yuantu',img)

# 全局阈值,整张图片使用一个固定的阈值二值化
# cv2.threshold(src,     # 输入图，只能输入单通道图像，通常来说为灰度图
#               thresh,  # 阈值
#               maxval,  # 当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值
#               type)    # 二值化操作的类型，包含以下5种类型： cv2.THRESH_BINARY；
#                          cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC；
#                          cv2.THRESH_TOZERO；cv2.THRESH_TOZERO_INV
ret, img_bw_all = cv2.threshold(img_gray,100,255,cv2.THRESH_BINARY)

# 输出
cv2.imshow('quanjuyuzhi', img_bw_all)

# 自适应阈值二值化
# cv2.adaptiveThreshold(src,          # 输入图
#                       maxval,       # 当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值
#                       thresh_type,  # 阈值的计算方法，包含以下2种类型：cv2.ADAPTIVE_THRESH_MEAN_C；
#                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C.
#                       type,         # 二值化操作的五中类型，与固定阈值函数相同
#                       Block Size,   # 图片中分块的大小
#                       C)            # 阈值计算方法中的常数项

img_bw_auto = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

cv2.imshow('zidongyuhzi',img_bw_auto)
cv2.waitKey(0)
