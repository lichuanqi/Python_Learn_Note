import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, QVariant, QUrl
from PyQt5.QtGui import QFont, QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLabel, QTextEdit, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QStatusBar

from PyQt5.QtMultimedia import QAudioRecorder, QAudioFormat, QSound, QSoundEffect


class UI_Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """中间主要区域"""

        # 窗体名称和尺寸
        self.setWindowTitle('录音机')
        self.resize(1000, 800)

        # 窗体位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 总体横向布局
        layout = QVBoxLayout()

        # 录音参数区域
        lo_params = QVBoxLayout()

        lo_params_device = QHBoxLayout()
        la_device = QLabel('录音设备:', self)
        self.cb_device = QComboBox()
        self.cb_device.setMinimumWidth(700)
        lo_params_device.addWidget(la_device)
        lo_params_device.addWidget(self.cb_device)
        lo_params_device.addStretch()

        lo_params_codec = QHBoxLayout()
        la_params_codec = QLabel('编码格式:', self)
        self.cb_codec = QComboBox()
        self.cb_codec.setMinimumWidth(700)
        lo_params_codec.addWidget(la_params_codec)
        lo_params_codec.addWidget(self.cb_codec)
        lo_params_codec.addStretch()

        lo_params_sample_rate = QHBoxLayout()
        la_sample_rate = QLabel('采 样 率:', self)
        self.cb_sample_rate = QComboBox()
        self.cb_sample_rate.setMinimumWidth(700)
        lo_params_sample_rate.addWidget(la_sample_rate)
        lo_params_sample_rate.addWidget(self.cb_sample_rate)
        lo_params_sample_rate.addStretch()

        lo_params_channal = QHBoxLayout()
        la_params_channal = QLabel('通 道 数:', self)
        self.cb_channal = QComboBox()
        self.cb_channal.setMinimumWidth(700)
        lo_params_channal.addWidget(la_params_channal)
        lo_params_channal.addWidget(self.cb_channal)
        lo_params_channal.addStretch()

        lo_params_container = QHBoxLayout()
        la_params_container = QLabel('视频格式:', self)
        self.cb_container = QComboBox()
        self.cb_container.setMinimumWidth(700)
        lo_params_container.addWidget(la_params_container)
        lo_params_container.addWidget(self.cb_container)
        lo_params_container.addStretch()

        lo_params_savepath = QHBoxLayout()
        la_params_container = QLabel('保存路径:', self)
        self.cb_savepath = QLineEdit()
        self.cb_savepath.setReadOnly(True)
        self.cb_savepath.setFixedWidth(700)
        self.cb_savepath.setPlaceholderText('请点击开始选择保存路径和文件名')
        lo_params_savepath.addWidget(la_params_container)
        lo_params_savepath.addWidget(self.cb_savepath)
        lo_params_savepath.addStretch()

        lo_params.addLayout(lo_params_device)
        lo_params.addLayout(lo_params_codec)
        lo_params.addLayout(lo_params_sample_rate)
        lo_params.addLayout(lo_params_channal)
        lo_params.addLayout(lo_params_container)
        lo_params.addLayout(lo_params_savepath)
        layout.addLayout(lo_params)
        layout.addSpacing(30)

        # 录音控制区域
        lo_control = QHBoxLayout()
        self.bt_start = QPushButton('开始')
        self.bt_end = QPushButton('结束')
        self.btn_play = QPushButton('播放')
        lo_control.addWidget(self.bt_start)
        lo_control.addWidget(self.bt_end)
        lo_control.addWidget(self.btn_play)
        lo_control.addStretch()
        layout.addLayout(lo_control)
        layout.addStretch()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 底部状态栏
        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage('初始化完成')
        self.setStatusBar(self.status_bar)


class RecordWindow(UI_Window):
    """主窗口"""
    def __init__(self) -> None:
        super().__init__()

        # 录音模块
        self.audioRecorder = QAudioRecorder()
        # 播放模块
        self.audioEffect = QSoundEffect()

        self.init_params()

    def init_params(self):
        # 槽函数
        self.cb_sample_rate.currentTextChanged.connect(self.update_sample_rate)
        self.audioRecorder.durationChanged.connect(self.update_recorder_time)

        self.bt_start.clicked.connect(self.start_)
        self.bt_end.clicked.connect(self.on_btn_end)
        self.btn_play.clicked.connect(self.on_btn_play)

        # 参数可选项
        self.cb_device.addItems(self.audioRecorder.audioInputs()) # 录音设备
        self.cb_codec.addItems(self.audioRecorder.supportedAudioCodecs()) # 编码方式
        samplerates, _ = self.audioRecorder.supportedAudioSampleRates() # 采样率 
        samplerates_str = [str(a) for a in samplerates]
        self.cb_sample_rate.addItems(samplerates_str)
        self.cb_channal.addItems(['1', '2'])
        self.cb_container.addItems(self.audioRecorder.supportedContainers()) # 视频格式
        
        # 设置参数默认值
        default_codec = self.audioRecorder.audioSettings().codec()
        default_sample_rate = self.audioRecorder.audioSettings().sampleRate()
        default_channal = self.audioRecorder.audioSettings().channelCount()
        default_container = self.audioRecorder.containerFormat()

        self.cb_codec.setCurrentText(default_codec)
        self.cb_sample_rate.setCurrentText(str(default_sample_rate))
        self.cb_channal.setCurrentText(str(default_channal))
        self.cb_container.setCurrentText(default_container)

    def start_(self):
        """录音 开始/结束"""
        if self.audioRecorder.state() == 0:
            # 选择文件保存名称
            savename, pathtype = QFileDialog.getSaveFileName(self, "文件保存", 
                    f"gui_pyqt/Audio_Record_PyQt/audio.wav" ,'wav(*.wav)')
            self.audioRecorder.setOutputLocation(QUrl.fromLocalFile(savename))
            self.cb_savepath.setText(savename)

            # 播放开始录音的提示音
            wav_sanmadi = wav_sanmadi = "resource/daomadi.wav"
            self.audioEffect.setSource(QUrl.fromLocalFile(wav_sanmadi))
            self.audioEffect.setLoopCount(1)
            self.audioEffect.setVolume(0.5)
            self.audioEffect.play()

            self.audioRecorder.record()
            print('开始录音')

        elif self.audioRecorder.state() == 1:
            self.audioRecorder.stop()
            print('正在录音中, 已停止')

        elif self.audioRecorder.state() == 2:
            self.audioRecorder.stop()
            print('录音暂停中, 已停止')

    def pause_(self):
        """录音 暂停/继续"""
        self.audioRecorder.pause()

    def on_btn_end(self):
        self.audioRecorder.stop()

    def on_btn_play(self):

        audio_file = self.cb_savepath.text()
        # 判断是否为空
        if audio_file is None:
            return False

        play_saomadi = QSound(audio_file, self)
        play_saomadi.play()


    def update_sample_rate(self):
        """采样率的下拉选框变化时更新参数"""
        sample_rate_new = self.cb_sample_rate.currentText()

        audio_format = QAudioFormat()
        audio_format.setSampleRate(int(sample_rate_new))

        if self.audioRecorder.state() == 0:
            print(f'采样率发生变化: {sample_rate_new}')
            print(self.audioRecorder.audioSettings().sampleRate())

    def update_recorder_time(self):
        """在状态栏显示录音时间"""
        duration = self.audioRecorder.duration()
        self.status_bar.showMessage(f'时间: {duration/1000}s')


if __name__ == '__main__':
    # 设置字体
    font = QFont()
    font.setFamily('宋体')
    font.setPointSize(12)

    app = QApplication(sys.argv)
    app.setFont(font)
    win = RecordWindow()
    win.show()
    sys.exit(app.exec_())