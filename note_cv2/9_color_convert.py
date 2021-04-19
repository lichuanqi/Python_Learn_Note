"""
图像颜色模式转换测试
lichuan
lc@dlc618.com
"""
import cv2


image = cv2.imread('/media/lcq/Data/modle_and_code/2_image/dongjiao_qing/960-540-222.jpg')
image_gray = cv2.cvtColor(image,cv2.COLOR_RGB2YUV)

image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
image_h, image_s, image_v = cv2.split(image_hsv)



# show
cv2.imshow('image_gray',image_gray)
cv2.imshow('image_h',image_h)
cv2.imshow('image_s',image_s)
cv2.imshow('image_v',image_v)

cv2.waitKey(0)
cv2.destroyAllWindows()
