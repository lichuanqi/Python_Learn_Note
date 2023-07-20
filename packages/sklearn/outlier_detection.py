"""
异常值检测算法
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

# 构造一组数据
data,_ = make_regression(n_samples=100,
                         n_features=2,
                         n_targets=1)
# 将第一行改为100作为异常值
data[0,:] = 10


# 局部离群因子LOF LocalOutlierFactor
# detector = LocalOutlierFactor(n_neighbors=2)

# 隔离森林 Isolation Forest
# detector = IsolationForest(n_estimators=10, warm_start=True)

# OneClassSVM
# detector = OneClassSVM()

# 鲁棒协方差估计 EllipticEnvelope
detector = EllipticEnvelope()

# 预测结构
predict = detector.fit_predict(data)


print(f'训练集所有数据点的离群结果为: {predict}')
# print(f'训练集所有数据点的LOF分为: {score.sum()}')

# 绘制散点图
plt.scatter(data[:,0], data[:,1], s=20, c=predict, marker='o')
plt.colorbar()
plt.show()