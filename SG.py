"""
Savitzky-Golay滤波器用于曲线平滑
lichuan
lc@dlc618.com
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


if __name__ == "__main__":
    
    # generate a set of data randomly 
    Size = 100
    x = np.linspace(0,2*np.pi,100)
    data = np.sin(x) + np.random.random(100) * 2
    print("input data:",data)

    # savgol_filter
    y = savgol_filter(data, 59, 3, mode= 'nearest')

    # plot
    plt.figure(1)
    plt.plot(x, data,color='y',label='pre_filter data')
    plt.plot(x, y, 'b', label = 'savgol_filter')
    # plt.plot(x, np.array(list), 'r', label = 'self')
    plt.legend()
    # plt.savefig("sg.png",dpi=600)
    plt.show()






