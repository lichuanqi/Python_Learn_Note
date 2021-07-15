"""
图像颜色模式转换测试
lichuan
lc@dlc618.com
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

SHOW = True
SAVE = False
save_path = '/media/lcq/Data/modle_and_code/3_expdata/20210521-HSV/'

image = cv2.imread('/media/lcq/Data/modle_and_code/2_image/shadow.jpg')
# image = cv2.imread('/media/lcq/Data/modle_and_code/2_image/dongjiao_qing/960-540-222.jpg')


image = cv2.pyrDown(image)

image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

image_gray = np.array(image_gray)
imin = np.min(np.min(image_gray))
imax = np.max(np.max(image_gray))
image_gray1 = ((image_gray-imin)/(imax-imin))*255
image_gray2 = np.array(image_gray1,dtype='uint8')

image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
image_h, image_s, image_v = cv2.split(image_hsv)

# FV = (image_h/360 + image_s + image_v)
# FV = np.array(FV,dtype='uint3')

# 中值滤波平滑处理
# image_gray_median = cv2.medianBlur(image_gray,5)
# image_v_median = cv2.medianBlur(image_v,7)

# show
if SHOW:
    cv2.imshow('image_gray',image_gray)
    cv2.imshow('image_gray1',image_gray2)
    # cv2.imshow('image_gray_median',image_gray_median)
    # cv2.imshow('image_h',image_h)
    # cv2.imshow('image_s',image_s)
    cv2.imshow('image_v',image_v)
    # cv2.imshow('FV',FV)
    # cv2.imshow('image_v_median',image_v_median)

    cv2.waitKey(0)

# plt.figure(figsize=131)
# plt.imshow(image_h)
# plt.figure(figsize=132)
# plt.imshow(image_s)
# plt.figure(figsize=133)
# plt.imshow(image_v)

# plt.show()


# save
if SAVE:
    name_image_gray = save_path + 'image_gray.jpg'
    cv2.imwrite(name_image_gray,image_gray)
    name_image_h = save_path + 'image_h.jpg'
    cv2.imwrite(name_image_h,image_h)
    name_image_s = save_path + 'image_s.jpg'
    cv2.imwrite(name_image_s,image_s)
    name_image_v = save_path + 'image_v.jpg'
    cv2.imwrite(name_image_v,image_v)

print('Finshed')
