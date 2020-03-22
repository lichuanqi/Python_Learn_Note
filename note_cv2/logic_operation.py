# 图像的逻辑运算

import cv2


# 读取二值化图像
fg_FD = cv2.imread('/media/lc/Data/modle_and_code/data/bgs-fd-only/fg-600.jpg',0)
fg_MOG = cv2.imread('/media/lc/Data/modle_and_code/data/cv-mog2-only/fg-300.jpg',0)
ret, fg_MOG = cv2.threshold(fg_MOG, 10, 255, cv2.THRESH_BINARY)
fg_MOG = cv2.medianBlur(fg_MOG, 5)

fg_add = cv2.bitwise_or(fg_MOG, fg_FD)

cv2.imshow('fg_FD', fg_FD)
cv2.imshow('fg_MOG', fg_MOG)

cv2.imshow('fg_add', fg_add)
cv2.waitKey(0)
