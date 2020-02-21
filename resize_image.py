'''
@Description: 缩放图片
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime : 2019-12-31 23:50:07
'''

import cv2
import numpy as np
import shutil
import os
 
 
infile = '/media/lc/Data/modle_and_code/data/m2.png'
image = cv2.imread(infile)

def resize_by_width(image,width_new):
    '''
    @description: 按照给定的宽度对图片进行所需比例的缩放操作
    @param {image}:读取后的图片
    @param {width_new}:想要得到的图片宽度
    @return: 处理后的图片
    '''
    x, y, z= image.shape
    print("图片尺寸为为：高度%d 宽度%d 维度%d"%(x, y, z))
    
    rate = width_new / y
    # resize函数输入宽度在前，高度在后 
    size = (int(y*rate), int(x*rate))
    img_new = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)  
    
    return img_new


# cv2.imshow('before',image)
cv2.imshow('after',resize_by_width(image,760))

cv2.waitKey(0)