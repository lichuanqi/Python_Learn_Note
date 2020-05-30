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
    plt.title('Part Compare')
    plt.plot(x, y)
    plt.xlabel('Frame')
    plt.ylabel('Object Number')
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

if __name__ == "__main__":
    xValue = list(range(0, 101))
    yValue = [x * np.random.rand() for x in xValue]

    plot_area(xValue, yValue)