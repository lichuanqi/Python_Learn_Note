import cv2
import numpy as np


def Contrast_and_Brightness(alpha, beta, img):
    """
    :param alpha: 调节对比度
    :param beta:调节亮度
    :param img:要调节的图像
    :return:调节后的图像
    """
    blank = np.zeros(img.shape, img.dtype)
    # dst = alpha * img + beta * blank
    dst = cv2.addWeighted(img, alpha, blank, 1-alpha, beta)
    return dst


if __name__ == '__main__':
    file_name = r'E:\model\data\300.jpg'
    img = cv2.imread(file_name)
    img_new_duibi_3 = Contrast_and_Brightness(1.3, 0, img)
    img_new_duibi_6 = Contrast_and_Brightness(1.6, 0, img)
    img_new_liangdu_1 = Contrast_and_Brightness(1, 20, img)
    img_new_liangdu_2 = Contrast_and_Brightness(1, 40, img)
    img_new = Contrast_and_Brightness(1.4, 10, img)

    cv2.imshow('yuan tu',img)
    cv2.imshow('add_duibi_1.3',img_new_duibi_3)
    cv2.imshow('add_duibi_1.6', img_new_duibi_6)
    cv2.imshow('add_liangdu_20',img_new_liangdu_1)
    cv2.imshow('add_liangdu_40', img_new_liangdu_2)
    cv2.imshow('img_new', img_new)

    #cv2.imwrite(r'E:\model\data\300_add_duibi_1.3.jpg',img_new_duibi_3)
    #cv2.imwrite(r'E:\model\data\300_add_duibi_1.6.jpg', img_new_duibi_6)
    #cv2.imwrite(r'E:\model\data\300_add_liangdu_20.jpg',img_new_liangdu_1)
    #cv2.imwrite(r'E:\model\data\300_add_liangdu_40.jpg', img_new_liangdu_2)
    cv2.imwrite(r'E:\model\data\300_add_duibi_liangdu.jpg', img_new)

    cv2.waitKey(0)