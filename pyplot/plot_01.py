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

    plt.title('Plot')
    # plt.plot(t, sc, label='sc')
    plt.plot(t, sc2, label='sc2')
    plt.xlabel('t', fontsize=16)
    plt.ylabel('sc', fontsize=16)
    plt.legend()
    plt.show()