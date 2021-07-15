'''
@Description: 
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-02-23 14:15:41
'''
import cv2

# 读取一张铁路场景的图片
imgpath = '/media/lc/Data/modle_and_code/data/m4.png'
img = cv2.imread(imgpath)

cv2.imshow('原图', img)

# 灰度化
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imshow('灰度化处理',img_gray)
cv2.waitKey(0)