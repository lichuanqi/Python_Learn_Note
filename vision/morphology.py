# 形态学处理
# 毕业论文第二章图片代码

import cv2
import os
from imageio import save


img_path = "D:/Code/Bgs_Tra/expdata/20220403-D11/20220403-D11400-3-foreground.jpg"
img = cv2.imread(img_path,0)

# 保存
is_show = False
is_save = True
save_path = 'D:/Code/Bgs_Tra/expdata/20220403-morphology'

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))  

if is_save and not os.path.exists(save_path):
    os.makedirs(save_path)
    print('保存路径不存在，已新建：{}'.format(save_path))

# 腐蚀
img_erode = cv2.erode(img, kernel)

# 膨胀
img_dilate = cv2.dilate(img, kernel)

# 开运算
img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# 闭运算
img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# show
if is_show:
    cv2.imshow('img_erode', img_erode)
    cv2.imshow('img_dilate', img_dilate)
    cv2.imshow('img_dilate', img_dilate)
    cv2.imshow('img_dilate', img_dilate)
    
    cv2.waitKey(0)

# save
if is_save:
    img_original_name = os.path.join(save_path, 'img_original.jpg')
    cv2.imwrite(img_original_name, img)
    img_erode_name = os.path.join(save_path, 'img_erode.jpg')
    cv2.imwrite(img_erode_name, img_erode)
    img_dilate_name = os.path.join(save_path, 'img_dilate.jpg')
    cv2.imwrite(img_dilate_name, img_dilate)
    img_open_name = os.path.join(save_path, 'img_open.jpg')
    cv2.imwrite(img_open_name, img_open)
    img_close_name = os.path.join(save_path, 'img_close.jpg')
    cv2.imwrite(img_close_name, img_close)

    print('已保存！')


