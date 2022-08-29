import cv2

# 读取视频，0为从摄像头获取，视频文件路径则为打开视频
cap = cv2.VideoCapture(0)

# 根据读取状态决定要不要继续
while cap.isOpened():
    # 逐帧读取
    # ret是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False。
    # frame就是每一帧的图像，是个三维矩阵
    ret, frame = cap.read()
    cv2.imshow('视频', frame)
    # 图像显示时间为 1 ms
    c = cv2.waitKey(1)
    # esc 键的ASC码为 27
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()