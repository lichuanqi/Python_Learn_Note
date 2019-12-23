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
    
    file_name = []

    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_name.append(root + file)
        return file_name
        
print(get_file_name(file_dir))