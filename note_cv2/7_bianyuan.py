# 边缘检测算法汇总

import cv2
import numpy as np

# 读取图片
img = cv2.imread('/media/lc/8A986A3C986A26C3/model/data/m4.png',0)

""""
canny
cv2.Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient ]]])   
必要参数：
第一个参数是需要处理的原图像，该图像必须为单通道的灰度图；
第二个参数是滞后阈值1；
第三个参数是滞后阈值2。
"""
img_canny = cv2.Canny(img, 30, 100)

"""
Laplacian
dst = cv2.Laplacian(src, ddepth[, dst[, ksize[, scale[, delta[, borderType]]]]])  
前两个是必须的参数：
第一个参数是需要处理的图像；
第二个参数是图像的深度，-1表示采用的是与原图像相同的深度。目标图像的深度必须大于等于原图像的深度；
其后是可选的参数：
dst不用解释了；
ksize是算子的大小，必须为1、3、5、7。默认为1。
scale是缩放导数的比例常数，默认情况下没有伸缩系数；
delta是一个可选的增量，将会加到最终的dst中，同样，默认情况下没有额外的值加到dst中；
borderType是判断图像边界的模式。这个参数默认值为cv2.BORDER_DEFAULT。
"""
Laplacian = cv2.Laplacian(img, cv2.CV_8U, img)






cv2.imshow("canny",img_canny)
cv2.imshow("Laplacian", Laplacian)

cv2.waitKey()
cv2.destroyAllWindows()