'''
@Description: 二值化图像灰度投影
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-03-08 21:21:41
'''

import cv2
import numpy as np  
from matplotlib import pyplot as plt  


# 读取图片，装换为可运算的数组
img=cv2.imread('/media/lc/Data/modle_and_code/data/paper2-1/499-3.jpg')  
# 将BGR图转为灰度图
GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# 二值化
ret,thresh1 = cv2.threshold(GrayImage,130,255,cv2.THRESH_BINARY)

(h,w) = thresh1.shape #返回高和宽

# 水平投影，像素值纵向累计
# 初始化一个长度为w的数组，用于记录每一列的像素累计
id_x = np.linspace(0, w, w, endpoint=False)
a = [0 for z in range(0, w)] 
 
# 记录每一列的波峰
for j in range(0,w): #遍历一列 
    for i in range(0,h):  #遍历一行
        if  thresh1[i,j] == 255:
            a[j]+=1 
            # thresh1[i,j] = 0  #记录完后将其变为白色 

# 展示累计灰度图 
# for j  in range(0,w):  #遍历每一列
#     for i in range((h-a[j]), h):  #从该列应该变黑的最顶部的点开始向最底部涂黑
#         thresh1[i,j] = 255   #涂黑


# 纵向投影　水平像素累计
id_y = np.linspace(h-1, 0, h, endpoint=True)
b = [0 for z in range(0, h)] 

# 每一行像素累加
for j in range(0,h):  
    for i in range(0,w):  
        if  thresh1[j,i] == 255: 
            b[j]+=1 
            # thresh1[j,i] = 0
         
# for j  in range(0,h):  
#     for i in range(0,a[j]):   
#         thresh1[j,i]=0    

# 展示
plt.figure(1)
plt.plot(id_x, a)

plt.figure(2)
plt.plot(b, id_y)

plt.show()