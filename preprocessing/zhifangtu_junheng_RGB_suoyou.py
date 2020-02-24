#
import cv2
import numpy as np

# 第一步：读入图片
mri_img = cv2.imread('/media/lc/8A986A3C986A26C3/model/data/m4.png')

r, c, h = mri_img.shape

for k in range(h):
    temp = mri_img[:,:,k]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(6,6))
    img = clahe.apply(temp)

cv2.imshow('mri', temp)
cv2.imshow('RGB junheng',img)
cv2.waitKey(0)
