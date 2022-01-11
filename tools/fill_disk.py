#!/usr/bin/python

import os,sys
import errno
import time

import numpy as np
from numpy import random
import cv2

import multiprocessing


def random_video():
    """
    功能：
        填充随机像素值的视频到一个视频文件
    """

    file_path = '/media/lcq/0000678400004823/AV_004.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter(file_path, fourcc, 25.0, (4096,3112), True)

    # Start 
    start_time = time.time()
    print('Start Time : %s'%(start_time))

    for i in range(0, 100000):
        
        print('%s...'%(i))

        zeros = np.ones(shape=(3112, 4096),dtype='uint8')
        frame_1 = random.randint(0,255,size=(3112, 4096),dtype='uint8')
        frame = cv2.merge([frame_1,zeros,frame_1])

        # cv2.imshow('frame', frame)
        # cv2.waitKey(2)

        output.write(frame)

    # End
    time_used = time.time()-start_time
    print('Time Used: %s'%(time_used))


def random_str(output_path):
    """
    功能：
        填充字符到一个文件
    """

    write_str = "!@#$%"*1024*1024*5  # 5MB
    
    with open(output_path, "w") as f:
        
        while True:
            try:
                f.write(write_str)
                f.flush()
            except IOError as err:
                if err.errno == errno.ENOSPC:
                    write_str_len = len(write_str)
                    if write_str_len > 1:
                        write_str = write_str[:write_str_len/2]
                    else:
                        print('Break')
                        break
                else:
                    print('Raise')
                    raise


if __name__ == '__main__':
    
    output_path = '/media/lcq/0000678400004823/3.txt'
    random_str(output_path)

    # pool_num = multiprocessing.Pool(4)
    # print('主进程：{0}'.format(os.getpid()))
    # print('子进程开始咯')

    # for i in range(5):

    #     output_path_i = '/media/lcq/0000678400004823/%s.txt'%(i+8)
    #     print(output_path_i)
    #     pool_num.apply_async(random_str, args=(output_path_i,))

    # pool_num.close()
    # pool_num.join()

    # print('子进程结束了')
    # print('主进程结束了')
