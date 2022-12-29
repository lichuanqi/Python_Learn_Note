'''
@Description: 缩放图片
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime : 2019-12-31 23:50:07
'''
from datetime import datetime
import cv2
import numpy as np


def image_resize(image:np.ndarray, width):
    '''图片尺寸缩放
    按照给定的宽度对图片进行所需比例的缩放操作
    
    Params 
        {image}    : 读取后的图片
        {width_new}: 想要得到的图片宽度
    
    Return
        img_new: 处理后的图片
    '''
    assert isinstance(image, np.ndarray), '请确定输入参数类型'

    h, w, n = image.shape
    
    # 计算缩放比例
    rate = width / w
    size = (int(w*rate), int(h*rate))
    img_new = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)  
    
    return img_new


if __name__ == '__main__':
    imfile = "D:/DATASET/ExpressBox/images/20221109_1500.jpg"
    image = cv2.imread(imfile)

    ts = datetime.now()
    img_new = image_resize(image, 200)
    tu = datetime.now() - ts
    print(f'Time Used: {tu}')

    # cv2.imshow('before', image)
    # cv2.imshow('after', img_new)
    # cv2.waitKey(0)