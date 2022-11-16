'''
@Description: 根据指定文件夹内的图片序列生成动图
@Autor: lichuan
@Email: lc@dlc618.com
@LastEditTime : 2019-12-23 13:16:32
'''

import imageio
import os


def create_gif(image_list, gif_name, duration = 1.0):
    '''
    生成动图函数
    :param image_list: 这个列表用于存放生成动图的图片
    :param gif_name: 字符串，所生成gif文件名，带.gif后缀
    :param duration: 图像间隔时间
    :return:
    '''
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))

    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)

    return


def get_file_name(file_dir):
    '''
    @description: 读取指定文件名称
    @param:file_dir:要读取图片的文件夹
    @return: 图片绝对路径列表
    '''
    file_name = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_name.append(root + file)
        return file_name


def main():

    file_dir = '/media/lc/Data/modle_and_code/新建文件夹/'
    image_list = get_file_name(file_dir)

    gif_name = 'new.gif'
    duration = 0.5
    create_gif(image_list, gif_name, duration)

if __name__ == '__main__':
    main()