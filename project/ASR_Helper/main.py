import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, QVariant, QUrl
from PyQt5.QtGui import QFont, QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QStyleFactory
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLabel, QTextEdit, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QStatusBar


class RecordWindow(QMainWindow):
    """主窗口"""
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
        self.init_params()

    def init_ui(self):
        """中间主要区域"""
        # 窗体名称和尺寸
        self.setWindowTitle('录音机')
        self.resize(1000, 800)

        # 窗体位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 总体横布局
        layout = QHBoxLayout()
        
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        gb_contrl = QGroupBox('控制区域')
        layout_contrl = QVBoxLayout(gb_contrl)
        label_api = QLabel('接口')
        lineedit_api = QComboBox()
        items_api = ['U2PP(本地)', 'U2PP(GPU服务器)']
        lineedit_api.addItems(items_api)
        button_select_file = QPushButton('选择文件')
        button_listen_microphone= QPushButton('监听麦克风')
        layout_contrl.addWidget(label_api)
        layout_contrl.addWidget(lineedit_api)
        layout_contrl.addWidget(button_select_file)
        layout_contrl.addWidget(button_listen_microphone)
        layout_left.addWidget(gb_contrl)

        gb_log = QGroupBox('日志区域')
        layout_log = QHBoxLayout(gb_log)
        edit_log = QTextEdit()
        layout_log.addWidget(edit_log)
        layout_left.addWidget(gb_log)

        gb_result = QGroupBox('识别结果')
        layout_result = QHBoxLayout(gb_result)
        edit_result = QTextEdit()
        layout_result.addWidget(edit_result)
        layout_right.addWidget(gb_result)

        layout.addLayout(layout_left)
        layout.addLayout(layout_right)
        layout.addSpacing(30)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 底部状态栏
        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage('初始化完成')
        self.setStatusBar(self.status_bar)

    def init_params(self):
        pass


if __name__ == '__main__':
    # 设置字体
    font = QFont('微软雅黑', 10)

    app = QApplication(sys.argv)
    app.setFont(font)
    win = RecordWindow()
    win.show()
    sys.exit(app.exec_())