'''
@Description: 
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-02-24 15:20:22
'''


import cv2
import numpy as np


# 第一步：读入图片
mri_img = cv2.imread('/media/lc/Data/modle_and_code/data/450.png')
r, c, h = mri_img.shape

for k in range(h):
    temp = mri_img[:,:,k]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(6,6))
    img = clahe.apply(temp)

cv2.imshow('mri', temp)
cv2.imshow('RGB junheng',img)
cv2.waitKey(0)
