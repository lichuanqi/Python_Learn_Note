"""
二位密度图
lichuan
lc@dlc618.com
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.font_manager import FontProperties


# 设置字体
times = FontProperties(fname='/home/lcq/.local/share/fonts/Times New Roman/times.ttf', size=18)

# 读取实验图片
image_01 = cv2.imread('/media/lcq/Data/modle_and_code/video/big_1080_16s/00_background.jpg',0)
image_01 = np.array(image_01)
image_02 = cv2.imread('/media/lcq/Data/modle_and_code/video/big_1080_16s/200_third.jpg',0)
image_02 = np.array(image_02)

# 作差
fd = abs(image_02 - image_01)
# 比值
ratio = image_02 / image_01


# 像素值核密度图
# plt.figure(1)
# cmap=cm.Set1_r #选择颜色系为蓝色体系
# plt.imshow(ratio,interpolation="nearest",cmap=cmap,aspect="auto",vmin=0,vmax=2)
# plt.xlabel('columns', FontProperties=times)
# plt.ylabel('rows', FontProperties=times)
# plt.xticks(FontProperties=times)
# plt.yticks(FontProperties=times)
# plt.colorbar()

# plt.savefig('/media/lcq/Data/modle_and_code/data/ratio-map-true.jpg',dpi=300, bbox_inches='tight')

# 像素值直方图
plt.figure(2)
plt.hist(fd, facecolor='blue', alpha=0.8)
plt.xlabel('pixel value ratio', FontProperties=times)
plt.ylabel('number', FontProperties=times)
plt.xticks(FontProperties=times)
plt.yticks(FontProperties=times)
plt.minorticks_on()
plt.xlim(0,2)

# plt.savefig('/media/lcq/Data/modle_and_code/data/ratio-hist-false.jpg',dpi=300, bbox_inches='tight')

plt.show()