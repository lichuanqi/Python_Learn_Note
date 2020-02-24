
import cv2
import numpy as np


# 第一步：读入图片
img = cv2.imread('/media/lc/8A986A3C986A26C3/model/data/m4.png')
print(img.dtype)
# rgb转ycbcr
img_y = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)

#　通道分离
y, cb, cr = cv2.split(img_y)

# 对Y通道进行自适应直方图均衡化函数
clahe= cv2.createCLAHE(clipLimit=2.0,
                        tileGridSize=(6, 6))
y_new  = clahe.apply(y)

# 三通道拼接并转换成rgb
img_new = cv2.merge([y_new, cb, cr])
img_new = cv2.cvtColor(img_new,cv2.COLOR_YCrCb2BGR)

# 灰度化处理
img_new_gray = cv2.cvtColor(img_new,cv2.COLOR_RGB2GRAY)

# 打印图像
cv2.imshow('yuantu', img)
cv2.imshow('zishiying', img_new)
cv2.imshow('zishiying_huiduhua', img_new_gray)
# cv2.imwrite('/media/lc/8A986A3C986A26C3/model/data/zishiying_huiduhua.jpg', img_new_gray)
# cv2.imwrite('/media/lc/8A986A3C986A26C3/model/data/zishiying.jpg', img_new)
cv2.waitKey(0)
cv2.destroyAllWindows()