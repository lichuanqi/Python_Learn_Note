# 在matlab中，存在执行直接得函数来添加高斯噪声和椒盐噪声。
# Python-OpenCV中虽然不存在直接得函数，但是很容易使用相关的函数来实现。

import numpy as np
import random
import cv2
import time

def noise_np(image, prob = 0.1):
    """添加椒盐噪声
    :param image: 要添加噪声的图像
    :param prob: 噪声比例
    :return: 添加噪声的图像
    """
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


def noise_gasuss(image, mean=0.01, var=0.002):
    """添加高斯噪声
    :param image:
    :param mean: 均值
    :param var: 方差
    :return:
    """
    image = np.array(image / 255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out * 255)
    return out


if __name__ == '__main__':
    img = r'E:\model\data\300.jpg'
    img = cv2.imread(img)

    #开始计时
    start = time.time()
    img_np = noise_np(img,0.1)
    time_used = time.time() - start
    print("Time used for add np noise: " + str(time_used))
    cv2.imshow('np',img_np)
    # cv2.imwrite('E:\model\data\origin_add_np_0.1.jpg',img_np)

    #开始计时
    start = time.time()
    img_np = noise_np(img, 0.1)
    time_used = time.time() - start
    print("Time used for add ga noise: " + str(time_used))
    img_ga = noise_gasuss(img, 0.03, 0.03)
    cv2.imshow('ga', img_ga)
    cv2.imwrite(r'E:\model\data\origin_add_ga.jpg', img_ga)

    cv2.waitKey(0)