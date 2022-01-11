#====================================
# Python读取和普威视红外摄像机rtsp码流并显示画面
# 2021.09.05
# lichuan，lc@dlc618.comn
#====================================


import  cv2


# 主码流
url = 'rtsp://admin:Abc.12345@192.168.1.65:554/h264/0/'
 
# 子码流
# url = 'rtsp://admin:Abc.12345@192.168.1.65:554/h264/ch1/main/av_stream'

cap = cv2.VideoCapture(url)

while(cap.isOpened()):  
 
    ret, frame = cap.read()  

    cv2.imshow('frame',frame)  
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break  
  
cap.release()  
cv2.destroyAllWindows()