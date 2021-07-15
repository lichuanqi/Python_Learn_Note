'''
@Description: 利用opencv-python像图片中添加文本
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-02-23 19:21:39
'''
import cv2


# 读取一张铁路场景的图片
imgpath = '/media/lc/Data/modle_and_code/data/m4.png'
img_origin = cv2.imread(imgpath)
img = img_origin.copy()

# 图片添加文本信息

font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText()函数
# 传入参数分别为：图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度
img = cv2.putText(img, 'Detected Number ：６', (30, 30), font, 0.9, (255, 255, 255), 2)
                  

cv2.imshow('img',img)
cv2.waitKey(0   )