##################################
# 利用最小二乘法拟合直线
# lichuan
# lc@dlc618.com
##################################

import numpy as np
from matplotlib import pyplot as plt


def fit(data_x, data_y):
    m = len(data_y)
    x_bar = np.mean(data_x)
    sum_yx = 0
    sum_x2 = 0
    sum_delta = 0
    for i in range(m):
        x = data_x[i]
        y = data_y[i]
        sum_yx += y * (x - x_bar)
        sum_x2 += x ** 2
    # 根据公式计算w
    w = sum_yx / (sum_x2 - m * (x_bar ** 2))

    for i in range(m):
        x = data_x[i]
        y = data_y[i]
        sum_delta += (y - w * x)
    b = sum_delta / m
    return w, b


if __name__=='__main__':

    # 模拟数据
    x = np.arange(1, 17, 1)
    y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 10.86, 10.00, 10.20, 10.32, 10.42, 10.50, 11.55, 12.58, 13.60])
    # 计算并绘制
    w, b = fit(x, y)
    pred_y = w * x + b
    plt.scatter(x, y)
    plt.plot(x, pred_y, c='r', label='line')
    plt.show()