'''
@Description: 读取视频并保存指定图像帧
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime: 2020-02-24 14:34:16
'''

import cv2
import time


# 相关函数
def resize_by_width(image,width_new):
    '''
    @description: 按照给定的宽度对图片进行所需比例的缩放操作
    @param {image}:读取后的图片
    @param {width_new}:想要得到的图片宽度
    @return: 处理后的图片
    '''
    x, y, z= image.shape
    rate = width_new / y
    # resize函数输入宽度在前，高度在后 
    size = (int(y*rate), int(x*rate))
    img_new = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)  
    
    return img_new


# 视频路径并读取
path = '/media/lc/Data/modle_and_code/data/video_02/30s.mp4'
cap = cv2.VideoCapture(path)

# 输出保存相关数据
# save_frame_no = []
save_frame_no = [1,10]
save_path = '/media/lc/Data/modle_and_code/data/'

# 参数赋值
i = 1                            # 视频帧计数器
time_start = time.time()         # 获取循环开始时间

while cap.isOpened():
    # 逐帧读取图片
    ret, frame = cap.read()

    # 图像金字塔
    frame_first = frame
    frame_second = cv2.pyrDown(frame)
    frame_third = cv2.pyrDown(frame_second)

    # 判断视频是否结束
    if ret == False:
        time_used = time.time() - time_start
        print('视频结束，总处理时间为 %f !'%time_used)
        break
    print('第 %d 张图片读取成功，正在处理中... ...'%i)

    # 图像数据保存到本地
    if i in save_frame_no:
        name_yuantu = save_path + str(i) + '.jpg'
        cv2.imwrite(name_yuantu, frame_second)
        print('----第 %d 帧图像保存到本地！'%i)

    i += 1


