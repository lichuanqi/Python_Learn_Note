"""
图像颜色模式转换测试
lichuan
lc@dlc618.com
"""
import cv2

SHOW = True
SAVE = False
save_path = '/media/lcq/Data/modle_and_code/3_expdata/20210521-HSV/'

image = cv2.imread('/media/lcq/Data/modle_and_code/3_expdata/20210518-Paper02Result/359-a-frame-origin.jpg')
image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# 中值滤波平滑处理
image_gray_median = cv2.medianBlur(image_gray,7)

image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
image_h, image_s, image_v = cv2.split(image_hsv)

image_v_median = cv2.medianBlur(image_v,7)

# show
if SHOW:
    cv2.imshow('image_gray',image_gray)
    cv2.imshow('image_gray_median',image_gray_median)
    cv2.imshow('image_h',image_h)
    cv2.imshow('image_s',image_s)
    cv2.imshow('image_v',image_v)
    cv2.imshow('image_v_median',image_v_median)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
