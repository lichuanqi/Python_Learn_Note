"""
Savitzky-Golay滤波器用于曲线平滑
lichuan
lc@dlc618.com
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def smooth_savgol_filter():

    # generate a set of data randomly 
    # Size = 100
    # x = np.linspace(0,2*np.pi,100)
    # y = np.sin(x) + np.random.random(100) * 2

    # 真实数据
    x = np.arange(0, 20, 1)
    y = np.array([
        0.00,
        0.00,
        0.00,
        0.00,
        0.00,
        0.00,
        0.00,
        0.00,
        0.00,
        76.05,
        44.01,
        37.96,
        33.40,
        34.55,
        35.34,
        28.90,
        38.61,
        39.39,
        0.00,
        43.55])
    
    print("input x:", x)
    print("input y:", y)

    # savgol_filter
    y_smooth = savgol_filter(y, 59, 3, mode= 'nearest')

    # plot
    plt.figure()
    plt.plot(x, y, color='y',label='pre_filter data')
    plt.plot(x, y_smooth, 'b', label = 'savgol_filter')
    plt.legend()
    # plt.savefig("sg.png",dpi=600)
    plt.show()


if __name__ == "__main__":
    smooth_savgol_filter()