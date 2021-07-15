"""
SciencePlots库测试
lichuan
lc@dlc618.com
"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,100,100)
y1 = np.random.randn()*x
y2 = np.random.randn()*x + 2

with plt.style.context(['science', 'ieee','no-latex']):
    plt.figure()
    plt.title('SciencePlots')
    plt.plot(x, y1,label='A')
    plt.plot(x, y2,label='B')
    plt.legend(title='Order')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()