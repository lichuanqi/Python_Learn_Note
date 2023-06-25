"""维度直方图
"""
import numpy as np
import matplotlib.pyplot as plt


xx = np.random.randn(100)
yy = np.random.randn(100)

def test_hist():
    plt.hist(xx)
    plt.show()


def test_hist2d():
    plt.hist2d(xx, yy, cmap='Blues')
    plt.colorbar()
    plt.show()


# test_hist()
test_hist2d()