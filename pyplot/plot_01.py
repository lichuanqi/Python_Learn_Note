'''
pyplot画图笔记
lichuan
lc@dlc618.com
'''

import numpy as np
import matplotlib.pyplot as plt


def plot_scatter(x, y):
    """
    簇状图
    """
    plt.title('plot scatter')
    plt.xlabel('x-value')
    plt.ylabel('y-label')
    plt.scatter(x, y, s=20, c="#ff1212", marker='o')
    plt.show()


def plot_line(x, y):
    """
    折线图
    """
    plt.title('Plot')
    plt.plot(x, y)
    plt.xlabel('t')
    plt.ylabel('sc')
    plt.show()

def plot_area(x, y):
    """
    填充图
    """
    plt.title('Part Compare')
    plt.fill_between(x, y)
    plt.xlabel('Frame')
    plt.ylabel('Object Number')
    plt.show()

def plot_rectangle():
    """
    矩形框
    输入：xy, width, height, angle=0.0， fill, linewidth=3, edgecolor="r"
        xy: 2元组 矩形左下角xy坐标
        width:矩形的宽度
        height:矩形的高度
        angle: float, 可选，矩形相对于x轴逆时针旋转角度，默认0
        fill: bool, 可选，是否填充矩形
    """
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis([-10,10, -10,10])
    rect = plt.Rectangle((0,0),4,8,fill=False,edgecolor="r")
    ax.add_patch(rect)

    plt.show()


if __name__ == "__main__":

    # xValue = list(range(0, 101))
    # yValue = [x * np.random.rand() for x in xValue]
    d = 0.4
    r = 0.2
    a = 33000
    c = 3000

    t = np.array(range(3, 10))
    sc = (t*(a-c)**2) / (2*(2*t-r**2))
    sc2 = t*(6*t*(1-d)**2-r**2)*(a-c)**2/2*(4*t*(1-d)-r**2)**2

    plot_rectangle()