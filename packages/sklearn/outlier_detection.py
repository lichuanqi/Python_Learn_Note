"""
离群点检测
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor


if __name__ == '__main__':
    data = np.array([[0,0], [1,2], [2,3], [3,3], [20,20]])
    point = np.array([[1,1]])

    data_std = data.std()

    # 筛选异常值
    clf = LocalOutlierFactor(n_neighbors=2)
    predict = clf.fit_predict(data)
    score = clf.negative_outlier_factor_

    print(f'训练集所有数据点的离群结果为: {predict}')
    print(f'训练集所有数据点的LOF分为: {score.sum()}')

    # 绘制散点图
    plt.scatter(data[:,0], data[:,1], s=20, c=predict, marker='o')
    plt.colorbar()
    plt.show()