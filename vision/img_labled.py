##################################
# 确定矩形框标注样式
# @lichuan
# @lc@dlc618.com
##################################

import cv2
import random

def label_img(img_dir):

    img = cv2.imread(img_dir)
    img_labled = img.copy()

    Color_list = [(255,0,0), (0,255,0),(0.0,255),
                     (153,50,4),(255,140,0)]
     
    boxColor = Color_list[random.randint(0,len(Color_list)-1)]

    cv2.rectangle(img_labled, (20, 30), (60, 90), boxColor, 2)
    cv2.putText(img_labled, str('persion') + " " + str(round(0.8777, 2)),
                (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, boxColor, 1)

    cv2.imshow('img', img_labled)
    cv2.waitKey(0)





if __name__ == '__main__':
    
    img_dir = '/media/lcq/Data/modle_and_code/TEMP/20210418-pf/pic2/001.jpg'
    
    label_img(img_dir)