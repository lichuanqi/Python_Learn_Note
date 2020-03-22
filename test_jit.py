'''
@Description: 测试numba.jit效果
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-03-12 16:14:20
'''
import time
import numpy as np
import numba as nb

import cv2


# @nb.jit()
def get_horizontal_projection(image, thresh=2):
    '''
    @Description:像素值水平投影
    @image:图像 
    @ret:是否绘制图像
    @return:no a分别为序号和累计像素值
    '''
    (h,w) = thresh1.shape #返回高和宽
    # 初始化一个长度为w的数组 ，用于记录每一列的像素累计
    a = [0 for z in range(0, w)]
    conditional_list = []
    
    # 记录每一列的波峰
    for j in range(0,w): #遍历一列 
        for i in range(0,h):  #遍历一行
            if  thresh1[i,j] == 255:
                a[j]+=1 
        if a[j] >= thresh:
            conditional_list.append(j)

    return a, conditional_list


# @nb.jit()
def ger_portrait_projection(image, thresh=2):
    '''
    @Description:像素值纵向投影
    @imaget：图像
    @return:
    '''    
    (h,w) = thresh1.shape #返回高和宽
    # 初始化一个长度为w的数组，用于记录每一列的像素累计
    b = [0 for z in range(0, h)] 
    conditional_list = []

    # 每一行像素累加
    for j in range(0,h):  
        for i in range(0,w):  
            if  thresh1[j,i] == 255: 
                b[j]+=1 
        if b[j] >= thresh:
            conditional_list.append(j)

    return b, conditional_list


# 读取二值化图像
img = cv2.imread('/media/lc/Data/modle_and_code/data/bgs-framedifference/600-fg.png',0)  

# 参数设定
horizontal_thresh = 1
portrait_thresh = 1

# 下采样，降低分辨率，加快速度
thresh1 = cv2.pyrDown(img)
tw, th = thresh1.shape
print('图片尺寸为：%s %s'%(tw, th))

time_start = time.time()

a, horizontal = get_horizontal_projection(thresh1, horizontal_thresh)
b, portrait = ger_portrait_projection(thresh1, portrait_thresh)

print(a)
print(b)

time_used = time.time() - time_start
print('Time used: %s' %time_used)