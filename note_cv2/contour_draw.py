#==============================================
# 提取二值化图像中的连通域轮廓信息
# lichuan
# lc@dlc618.com
# 2021.7.2
#==============================================

import cv2


if __name__ == '__main__':

    img = cv2.imread('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/aug_jpgs/rs00012_aug_0.jpg')
    mask = cv2.imread('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/aug_masks/rs00012_aug_0.png',0)

    mask = mask * 255

    ret, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

    cv2.imshow('img',img)
    cv2.waitKey(0)