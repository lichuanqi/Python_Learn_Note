#==============================================
# 提取二值化图像中连通域的轮廓信息
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
    
    img_fill = img.copy()
    for i in range(len(contours)):
        # 轮廓
        # cv2.drawContours(img, contours[i], -1, (0, 0, 255), 3)
        # 内部填充
        cv2.fillConvexPoly(img_fill, contours[i], (0, 0, 255))

    img_viz = cv2.addWeighted(img, 0.6, img_fill, 0.4, 0)

    cv2.imshow('img',img_viz)
    cv2.waitKey(0)