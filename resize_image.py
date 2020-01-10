'''
@Description: 
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime : 2019-12-31 23:50:07
'''

import cv2
import numpy as np
import shutil
import os
 
 
infile = '/media/lc/Data/网站/草稿-2019/Ｄeepin系统/deepin.png'
outfile = '/media/lc/Data/网站/草稿-2019/Ｄeepin系统/deepin_new.png'

def resize_by_width(infile,outfile,width_new):
    '''
    @description: 按照宽度进行所需比例缩放
    @param {infile}:输入图片路径和名称
    @param {outfile}:图片路径和名称
    @param {w_divide_h}:
    @return: 
    '''
    im = cv2.imread(infile)
    x, y, z= im.shape
    print("读取到的图片尺寸为：%d %d %d"%(x, y, z))
    
    rate = width_new / y
    x_new, y_new = x*rate, width_new
    im_new = np.zeros(x_new, y_new, z)  
    
    cv2.imwrite()


resize_by_width(infile,outfile,760)