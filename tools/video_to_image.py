'''
@Description: 读取视频并保存指定图像帧
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-02-24 14:34:16
'''
import os
import glob
import sys
from loguru import logger

import cv2
import time


def resize_by_width(image,width_new):
    '''
    按照给定的宽度对图片进行所需比例的缩放操作
    Args
        image       : 读取后的图片
        width_new   : 想要得到的图片宽度
    Return:
        img_new : 处理后的图片
    '''
    x, y, z= image.shape
    rate = width_new / y
    # resize函数输入宽度在前，高度在后 
    size = (int(y*rate), int(x*rate))
    img_new = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)  
    
    return img_new


def crop_image(img, x1, y1, x2,y2):
    """
    根据坐上角坐标和右小角坐标裁剪单张图像
    Args
        img   :原图
        x1,y1 :左上角坐标
        x2,y2 :左上角坐标
    """
    return img[y1:y2, x1:x2]


def crop_dir():
    """
    剪裁文件夹内的所有图像
    """
    
    dir = 'D:/Data/Expressbox/images/20221109'
    x1, y1, x2, y2 = 630,280,1920,1080
    save_path = 'D:/Data/Expressbox/images_crop/'

    imgs = glob.glob(dir + '*.jpg')

    for img in imgs:

        image = cv2.imread(img)

        # 保存路径
        name = os.path.basename(img)
        savename = os.path.join(save_path, name) 

        img_new = crop_image(image, x1, y1, x2,y2)
        cv2.imwrite(savename, img_new)
        logger.info(f'{img} -> {savename}')


def test(img, x1, y1, x2,y2):
    img = cv2.imread('D:/Data/Expressbox/images/20221109_750.jpg')
    x1, y1, x2, y2 = 630,280,1920,1080
    img_new = crop_image(img, x1, y1, x2,y2)


def video2img():
    # 视频路径
    path = 'D:/Data/Expressbox/v1.mp4'
    # 裁剪区域
    is_crop = False
    x1, y1, x2, y2 = 630,280,1920,1080
    # 保存时间间隔 单位(s)
    n = 1
    # 保存路径
    save_path = 'D:/Data/Expressbox/images/net01_'

    # 读取视频及属性
    cap = cv2.VideoCapture(path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   #获取原视频的宽
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #获取原视频的搞
    fps = int(cap.get(cv2.CAP_PROP_FPS))             #帧率
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))       #视频的编码
    logger.info(f'视频宽度: {width}, 高度: {height}, 帧率: {fps}')

    i = 0
    img_num = 0
    time_start = time.time()
    while cap.isOpened():
        # 逐帧读取图片
        ret, frame = cap.read()

        # 判断视频是否结束
        if not ret:
            time_used = time.time() - time_start
            logger.info(f'视频结束, 时间{time_used}, 图片数量{img_num}')
            break
        logger.info(f'第 {i}张图片读取成功.')

        # 判断是否保存
        if i%(25*n) == 0:

            # 图像裁剪
            if is_crop:
                img_new = crop_image(frame, x1, y1, x2, y2)
            else:
                img_new = frame

            # 保存
            savename = f'{save_path}{i}.jpg'
            cv2.imwrite(savename, frame)
            img_num += 1
            logger.info(f'第 {i} 帧图像已保存: {savename}')

        # 图像的展示
        # cv2.imshow('frame',frame)
        key = cv2.waitKey(1)
        if key == ord(' ') or key == ord('q'):
            break

        i += 1

    cap.release() #释放视频
    cv2.destroyAllWindows() #释放所有显示图像的窗口


if __name__=='__main__':

    video2img()

