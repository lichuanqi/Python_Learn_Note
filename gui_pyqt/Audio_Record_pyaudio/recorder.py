import sys
import pyaudio
import wave
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QStatusBar


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.result = ''

    def run(self):
        self.result = self.func(*self.args)
        
    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None


class Recorder():
    def __init__(self) -> None:
        # 录音参数
        self.recording = False  # 是否正在录音
        self.start_time = 0     # 录音开始时间
        self.end_time = 0       # 录音结束时间
        self.record_frames = [] # 音频数据

    def start(self):
        """开始录音"""
        if self.recording:
            return ''
        
        self.recording = True
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)

        while self.recording:
            data = stream.read(1024)
            self.record_frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()
        
    def start_thread(self):
        """开辟一个线程录音"""
        record_thread = MyThread(self.start)
        record_thread.start()

    def pause(self):
        """暂停录音"""
        pass

    def stop_and_save(self, savename):
        """结束录音"""
        if not self.recording:
            return ''

        # 保存音频文件
        p = pyaudio.PyAudio()
        wf = wave.open(savename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(self.record_frames))
        wf.close()

        # 录音参数重置
        self.recording = False
        self.record_frames = []

    def get_data():
        """获取音频文件"""


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.recorder = Recorder()

        self.init_UI()

        

    def init_UI(self):
        # 设置窗体名称和尺寸
        self.setWindowTitle('录音助手')
        self.resize(200, 100)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 创建总体横向布局
        layout = QVBoxLayout()

        kongzhi_layout = QHBoxLayout()
        bt_start = QPushButton('开始')
        bt_end = QPushButton('结束')
        kongzhi_layout.addWidget(bt_start)
        kongzhi_layout.addWidget(bt_end)
        kongzhi_layout.addStretch()
        layout.addLayout(kongzhi_layout)
        layout.addStretch

        bt_start.clicked.connect(self.bt_start_clicked)
        bt_end.clicked.connect(self.bt_stop_clicked)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
        # 底部状态栏
        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage('初始化完成')
        self.setStatusBar(self.status_bar)

    def bt_start_clicked(self):
        self.recorder.start_thread()
        self.status_bar.showMessage('录音中')

    def bt_stop_clicked(self):
        savename = 'gui_pyqt/Audio_Record_pyaudio/audio.wav'
        self.recorder.stop_and_save(savename)
        self.status_bar.showMessage('录音结束')
        

if __name__ == '__main__':
    # 设置字体
    font = QFont()
    font.setFamily('宋体')
    font.setPointSize(12)

    app = QApplication(sys.argv)
    app.setFont(font)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())