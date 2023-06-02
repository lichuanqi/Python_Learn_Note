# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the Dynamic Spline example from Qt v5.x"""
import sys
import random

from PySide6.QtCharts import QChart, QChartView, QSplineSeries, QValueAxis
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QPainter, QFont, QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtWidgets import QLabel


class get_latest_temp():
    """获取最新的温湿度数据"""


class MyWindow(QMainWindow):
    """主窗口"""
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗体名称,尺寸,位置
        self.setWindowTitle('动态表格')
        self.resize(600, 400)

        # 总体横向布局
        layout = QVBoxLayout()
        
        label_now = QLabel('当前时间: ')
        layout.addWidget(label_now)

        chart = Chart()
        chart.setTitle("Dynamic spline chart")
        chart.legend().hide()
        chart.setAnimationOptions(QChart.AllAnimations)
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # self.setCentralWidget(chart_view)


class Chart(QChart):
    def __init__(self, parent=None):
        super().__init__(QChart.ChartTypeCartesian, parent, Qt.WindowFlags())
        self._timer = QTimer()
        self._series = QSplineSeries(self)
        self._titles = []
        self._axisX = QValueAxis()
        self._axisY = QValueAxis()
        self._step = 0
        self._x = 5
        self._y = 1

        self._timer.timeout.connect(self.handleTimeout)
        self._timer.setInterval(1000)

        green = QPen(Qt.red)
        green.setWidth(3)
        self._series.setPen(green)
        self._series.append(self._x, self._y)

        self.addSeries(self._series)
        self.addAxis(self._axisX, Qt.AlignBottom)
        self.addAxis(self._axisY, Qt.AlignLeft)

        self._series.attachAxis(self._axisX)
        self._series.attachAxis(self._axisY)
        self._axisX.setTickCount(5)
        self._axisX.setRange(0, 10)
        self._axisY.setRange(-5, 10)

        self._timer.start()

    @Slot()
    def handleTimeout(self):
        x = self.plotArea().width() / self._axisX.tickCount()
        y = (self._axisX.max() - self._axisX.min()) / self._axisX.tickCount()
        self._x += y
        self._y = random.uniform(0, 5) - 2.5
        self._series.append(self._x, self._y)
        self.scroll(x, 0)
        if self._x == 100:
            self._timer.stop()


if __name__ == "__main__":

    # 设置字体
    font = QFont()
    font.setFamily('宋体')
    font.setPointSize(12)

    a = QApplication(sys.argv)
    a.setFont(font)
    window = MyWindow()
    window.show()

    sys.exit(a.exec())