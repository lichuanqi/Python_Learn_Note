import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, QVariant, QUrl
from PyQt5.QtGui import QFont, QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QLabel, QTextEdit, QLineEdit, QComboBox, QCheckBox
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QStatusBar
from PyQt5.QtWidgets import QStyle, QStyleOptionButton
from PyQt5.QtMultimedia import QAudioRecorder, QAudioFormat


class NewTableWidget(QTableWidget):
    """新的TableWidget类
    
    Params
        rows: 默认行数
        cols: 默认列数
        headers: 表头
    """
    def __init__(self, rows, cols, headers) -> None:
        super(NewTableWidget, self).__init__(rows, cols)
        # 交叉颜色
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)

        # 表头
        self.headers = headers
        self.init_headers()
        self.inport_data_sample()

    def init_headers(self):
        """初始化表头"""
        for i, info in enumerate(self.headers):
            item = QTableWidgetItem(info['name'])
            self.setHorizontalHeaderItem(i, item)
            self.setColumnWidth(i, info['width'])

    def table_add_row(self):
        """在末尾增加一行空白行"""
        table_count = self.rowCount()
        # 序列号
        self.insertRow(table_count)
        xuliehao = QTableWidgetItem(str(table_count))
        self.setItem(table_count, 0, xuliehao)
        # 删除按键
        shanchu = QPushButton('删除')
        shanchu.clicked.connect(self.table_delete_row)
        self.setCellWidget(table_count, 4, shanchu)

    def table_delete_row(self):
        """触发表格每一行的删除按钮时删除所在行"""
        button = self.sender()
        if button:
            rowid = self.indexAt(button.pos()).row()
            self.removeRow(rowid)

    def table_clear(self):
        """清空表格内容"""
        table_count = self.rowCount()
        if table_count > 0:
            self.setRowCount(0)
            self.clearContents()

    def inport_data(self):
        """数据导入"""
        pass

    def export_data():
        """数据导出"""
        pass

    def inport_data_sample(self):
        """给表格增加一些数据"""
        datalist = [
            ['1号', '男', '60'],
            ['2号', '女', '50'],
        ]
        table_count = self.rowCount()
        for i,data in enumerate(datalist):
            self.insertRow(table_count)
            xuliehao = QTableWidgetItem(str(table_count))
            self.setItem(table_count, 0, xuliehao)
            xingming = QTableWidgetItem(data[0])
            self.setItem(table_count, 1, xingming)
            xingbie = QTableWidgetItem(data[1])
            self.setItem(table_count, 2, xingbie)
            tizhong = QTableWidgetItem(data[2])
            self.setItem(table_count, 3, tizhong)
            shanchu = QPushButton('删除')
            shanchu.clicked.connect(self.table_delete_row)
            self.setCellWidget(table_count, 4, shanchu)
            table_count += 1


class TableWindow(QMainWindow):
    """主窗口"""
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """中间主要区域"""

        # 设置窗体名称,尺寸,位置
        self.setWindowTitle('表格操作')
        self.resize(1000, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 总体横向布局
        layout = QVBoxLayout()

        # 表格名称及操作区
        layout_name = QHBoxLayout()
        la_device = QLabel('表格名称:', self)
        layout_name.addWidget(la_device)
        layout_name.addStretch()
        buttom_add = QPushButton('增加一行')
        layout_name.addWidget(buttom_add)
        buttom_clear = QPushButton('清空')
        layout_name.addWidget(buttom_clear)
        buttom_inport = QPushButton('导入')
        layout_name.addWidget(buttom_inport)
        buttom_export = QPushButton('导出')
        layout_name.addWidget(buttom_export)

        # 表格区域
        headers = [
            {'name': 'No.', 'width':60},
            {'name':'姓名', 'width':200},
            {'name':'身高', 'width':200},
            {'name':'体重(kg)', 'width':200},
            {'name':'操作', 'width':200},
        ]
        self.table = NewTableWidget(0, 5, headers)
        self.table.itemChanged.connect(self.tableUpdate)

        # 给按钮绑定动作
        buttom_add.clicked.connect(self.table.table_add_row)
        buttom_clear.clicked.connect(self.table.table_clear)
        buttom_inport.clicked.connect(self.table.inport_data_sample)

        layout.addLayout(layout_name)
        layout.addWidget(self.table)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 底部状态栏
        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage('初始化完成')
        self.setStatusBar(self.status_bar)

    def tableUpdate(self, item:QTableWidgetItem):
        row, column = item.row(), item.column()
        print('table item changed', row, column)


if __name__ == '__main__':
    # 设置字体
    font = QFont()
    font.setFamily('宋体')
    font.setPointSize(12)

    app = QApplication(sys.argv)
    app.setFont(font)
    win = TableWindow()
    win.show()
    sys.exit(app.exec_())