'''
@Description: 帧差法确定候选区
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-03-05 10:56:43
'''

import cv2
import numpy as np


def resize_by_width(image,width_new):
    '''
    @description: 按照给定的宽度对图片进行所需比例的缩放操作
    @param {image}:读取后的图片
    @param {width_new}:想要得到的图片宽度
    @return: 处理后的图片
    '''
    x, y, z= image.shape
    
    rate = width_new / y
    # resize函数输入宽度在前，高度在后 
    size = (int(y*rate), int(x*rate))
    img_new = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)  
    
    return img_new


kernel_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel_2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
font = cv2.FONT_HERSHEY_SIMPLEX

# 读取
original = cv2.imread('bw2_original.png')
img = cv2.imread('bw2.png')

original = resize_by_width(original,1000)
img = resize_by_width(img,1000)

# 二值化
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(img,1,255,cv2.THRESH_BINARY)

# 形态学处理
img = cv2.dilate(img, kernel_1)  # 膨胀

# 降噪
img = cv2.medianBlur(img, 7)

# 连通域检测
ret, contours, her= cv2.findContours(img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

# 最大候选区坐标储存
min_x = 3000
min_y = 3000
max_x = 0
max_y = 0

for contour in contours:
    # 获取矩形框坐标数据
    x, y, w, h = cv2.boundingRect(contour)

    # 根据坐标在原图截取相应区域,y坐标,x坐标
    contour_area = img[y:y+h, x:x+w]
    area = cv2.countNonZero(contour_area)

    # 根据实际占有像素面积和假设的真实面积计算填充率
    rectangle_area = w * h
    fill_rate = area / rectangle_area

    if fill_rate <= 0.5:
        # 更新最大候选坐标
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(max_x, x+w)
        max_y = max(max_y, y+h)

        # 根据坐标绘制矩形框
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)
        
        # 添加填充率数值
        text = str(format(area/rectangle_area, '.2f'))
        cv2.putText(img, text, (x+w+3, y+h+3), font, 0.4, (255, 255, 255), 1)

# 最大候选区
# cv2.rectangle(original, (min_x, min_y), (max_x,  max_y), (255, 0, 0),2)
# cv2.rectangle(img, (min_x, min_y), (max_x,  max_y), (255, 0, 0),2)

# 展示
cv2.imshow('img',img)
cv2.imshow('original',original)

# 保存本地
# cv2.imwrite('img_frame_diff/bw2_candidate_0.5.png', img)
# cv2.imwrite('img_frame_diff/bw2_original_candidate_0.5.png',original)

cv2.waitKey(0)