'''
@Description: 读取路径内的文件名称
@Autor: lichuan
@Date: 1970-01-01 08:00:00
@LastEditors  : lichuan
@LastEditTime : 2019-12-23 12:52:48
'''

import os


# 保存不同模型的目录名(绝对路径)
file_dir = '/media/lc/Data/modle_and_code/新建文件夹/'

file_name = []

def get_file_name(file_dir):
    """
    获取指定文件夹内的文件名称
    file_dir：文件夹地址
    file_name：读取到的文件绝对地址
    """
    
    file_name = []

    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_name.append(root + file)
        return file_name
        

def write_file_name(file_name, txt_name):
    """
    将读取到的文件名称写入txt文件中
    file_name:读取到的文件名称
    txt_name：输出文件地址
    """
    
    for name in file_name:
        with open (txt_name, 'a') as f:
            f.write(name + '\n')


if __name__ == "__main__":

    file_dir = '/media/lc/Data/modle_and_code/data/image/'
    txt_name = '/media/lc/Data/modle_and_code/env_linux/yolov4/images.txt'

    file_name = get_file_name(file_dir)
    write_file_name(file_name, txt_name)
