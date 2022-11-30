import  cv2


url = 'rtsp://hik:rtsp.147@192.168.9.11:554/Streaming/Channels/102'


cap = cv2.VideoCapture(url)

while(cap.isOpened()):  
 
    ret, frame = cap.read()  
    cv2.imshow('frame',frame)  
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break  

cap.release()  
cv2.destroyAllWindows()