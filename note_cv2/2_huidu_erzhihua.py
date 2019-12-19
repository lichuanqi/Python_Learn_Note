import cv2

# 读取一张铁路场景的图片
imgpath = r'E:\model\data\300_add_liangdu_40.jpg'
img = cv2.imread(imgpath,1)

# ------- 定义结构元素 -------
# 椭圆
tuoyuan = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
# 矩形
juxing = cv2.getStructuringElement(cv2.MORPH_RECT,(6,3))

#输出显示
print('tuoyuan------------\n', tuoyuan)
print('juxing-------------\n', juxing)

cv2.imshow('原图', img)

# 灰度化
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imshow('灰度化处理',img_gray)
cv2.imwrite(r'E:\model\data\300_add_liangdu_40_huiduhua.jpg',img_gray)
cv2.waitKey(0)

# =========================================
# ================ 二值化 ==================
# 全局阈值,整张图片使用一个固定的阈值二值化
# cv2.threshold(src,     # 输入图，只能输入单通道图像，通常来说为灰度图
#               thresh,  # 阈值
#               maxval,  # 当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值
#               type)    # 二值化操作的类型，包含以下5种类型： cv2.THRESH_BINARY；
#                          cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC；
#                          cv2.THRESH_TOZERO；cv2.THRESH_TOZERO_INV
img_bw_all = cv2.threshold(img_gray,100,255,cv2.THRESH_BINARY)

# 输出
cv2.imshow('二值化-全局阈值', img_bw_all)
cv2.waitKey(0)

# 自适应阈值二值化
# cv2.adaptiveThreshold(src,          # 输入图
#                       maxval,       # 当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值
#                       thresh_type,  # 阈值的计算方法，包含以下2种类型：cv2.ADAPTIVE_THRESH_MEAN_C；
#                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C.
#                       type,         # 二值化操作的五中类型，与固定阈值函数相同
#                       Block Size,   # 图片中分块的大小
#                       C)            # 阈值计算方法中的常数项

img_bw_auto = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    11,2)
cv2.imshow('二值化-自动阈值',img_bw_auto)
cv2.waitKey(0)
