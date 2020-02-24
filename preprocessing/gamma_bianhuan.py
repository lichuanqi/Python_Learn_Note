import cv2
import numpy as np
import matplotlib.pyplot as plt


#分道计算每个通道的直方图
img = cv2.imread('/media/lc/8A986A3C986A26C3/model/data/m4.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#img_b, img_g, img_r = np.split(img)
# hist_b = cv2.calcHist([img0],[0],None,[256],[0,256])
# hist_g = cv2.calcHist([img0],[1],None,[256],[0,256])
# hist_r = cv2.calcHist([img0],[2],None,[256],[0,256])


def gamma_trans(img,gamma):
    #具体做法先归一化到1，然后gamma作为指数值求出新的像素值再还原
    gamma_table = [np.power(x/255.0,gamma)*255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    #实现映射用的是Opencv的查表函数
    return cv2.LUT(img,gamma_table)


img_corrted = gamma_trans(img_gray, 0.8)
cv2.imshow('img',img)
cv2.imshow('img_gray',img_gray)
cv2.imshow('gamma_image',img_corrted)
cv2.waitKey(0)