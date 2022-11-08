#====================================
# Python读取海康摄像机rtsp码流并显示画面
# 2021.06.24
# lichuan，lc@dlc618.comn
#====================================


import  cv2


# 主码流
url = 'rtsp://admin:hik12345+@192.168.9.11:554/h264/ch1/main/av_stream'
 
# 子码流
# url = 'rtsp://admin:hik12345+@192.168.9.11:554/h264/ch1/sub/av_stream'

cap = cv2.VideoCapture(url)

while(cap.isOpened()):  
 
    ret, frame = cap.read()  

    cv2.imshow('frame',frame)  
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break  
  
cap.release()  
cv2.destroyAllWindows()