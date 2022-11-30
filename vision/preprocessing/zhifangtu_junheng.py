
import cv2
import numpy as np



# 传统像素点直方图的均衡化
# 第一步：读入图片
img = cv2.imread('/media/lc/8A986A3C986A26C3/model/data/m4.png',0)

# 第二步: 使用cv2.equalizeHist实现像素点的均衡化
ret = cv2.equalizeHist(img)


# 第三步：进行图像的展示
cv2.imshow('yuantu', ret)
cv2.imwrite('quanjujunheng.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()