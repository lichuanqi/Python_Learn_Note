import time
import numpy as np
import  cv2

from queue import Queue
from threading import Thread


# 大平面
RTSP_DPM_MAIN = 'rtsp://hik:rtsp.147@192.168.9.11:554/Streaming/Channels/101'
RTSP_DPM_SUB = 'rtsp://hik:rtsp.147@192.168.9.11:554/Streaming/Channels/102'

# 海康普通
RTSP_HK_MAIN = 'rtsp://admin:hik12345+@192.168.9.11:554/h264/ch1/main/av_stream'
RTSP_HK_SUB = 'rtsp://admin:hik12345+@192.168.9.11:554/h264/ch1/sub/av_stream'

# 红外
RTSP_HW_MAIN = 'rtsp://admin:Abc.12345@192.168.1.65:554/h264/0/'
RTSP_HW_SUB= 'rtsp://admin:Abc.12345@192.168.1.65:554/h264/ch1/main/av_stream'

# 本地视频
VIDOE_1 = 'D:/DATASET/ExpressBox/videos/11_202211091706.mp4'


def read_rtsp():
    """使用cv2.VideoCapture读取RTSP视频流或本地视频"""

    cap = cv2.VideoCapture(RTSP_DPM_SUB)
    while(cap.isOpened()):  
    
        ret, frame = cap.read()  
        cv2.imshow('frame',frame)  
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break  
    
    cap.release()  
    cv2.destroyAllWindows()


class read_video_thread():
    """使用多线程和队列读取视频

    Example
        >>> frame_queue = Queue()
        >>> th = read_video_thread(frame_queue, VIDOE_1)
        >>> th.start()

    Params
        frame_queue : 保存视频帧的队列
            >>> from queue import Queue
            >>> frame_queue = Queue()
        video_url   : RTSP或本地视频地址
    """
    def __init__(self, frame_queue, video_url):

        self.frame_queue = frame_queue
        self.is_running = False  # 状态标签
        self.cam = cv2.VideoCapture(video_url)

        # 视频基本信息
        width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cam.get(cv2.CAP_PROP_FPS))
        print(f'视频基本信息: width={width}, height={height}, fps={fps}')
 
    def capture_queue(self):
        # 捕获图像
        while self.is_running and self.cam.isOpened():
            ret, frame = self.cam.read()
            
            if not ret:
                break
            else: 
                self.frame_queue.put(frame)
                print(f'图像数据已保存至队列, qsize={self.frame_queue.qsize()}')
 
    def start_(self):
        self.is_running = True
        self.thread_capture = Thread(target=self.capture_queue)
        self.thread_capture.start()
 
    def stop(self):
        self.is_running = False
        self.cam.release()


class show_image_thread():
    """使用多线程显示队列中的图像
    
    Params
        frame_queue : 保存图像的队列
    """
    def __init__(self, frame_queue):
        self.frame_queue = frame_queue
        self.none_times = 0
        self.none_times_max = 10

    def show_image(self):
        while True:
            # 根据实际需求，设置跳出循环（结束线程）的方法
            queue_size = frame_queue.qsize()

            if self.none_times > self.none_times_max:
                print('超过最大等待时间, 已停止')
                break

            elif queue_size <= 0:
                print(f'队列为空, 开始等待')
                time.sleep(2)
                self.none_times += 1
                continue
            
            else:
                self.none_times = 0
                image = frame_queue.get()
                cv2.namedWindow("camera", cv2.WINDOW_AUTOSIZE)    
                cv2.imshow("camera", image)

                frame_queue.task_done()
            
            if cv2.waitKey(40)& 0xFF == ord('q'): 
                break
    
    def start_(self):
        self.is_running = True
        self.thread_capture = Thread(target=self.show_image)
        self.thread_capture.start()


if __name__ == '__main__':
    # read_rtsp()

    # 新建队列保存数据
    frame_queue = Queue()
    frame_queue.maxsize = 5

    # 多线程读取视频流到队列
    th1 = read_video_thread(frame_queue, VIDOE_1)
    th1.start_()

    # 多线程显示
    th2 = show_image_thread(frame_queue)
    th2.start_()