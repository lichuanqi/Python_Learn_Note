"""
离群点检测
"""
import numpy as np
from sklearn.neighbors import LocalOutlierFactor


if __name__ == '__main__':
    data = np.array([[0,0], [1,2], [2,3], [3,3]])
    point = np.array([[1,1]])

    data_std = data.std()
    print(data_std)

    clf = LocalOutlierFactor(n_neighbors=2)
    predict = clf.fit_predict(data)
    score = clf.negative_outlier_factor_

    print(predict)
    print(score)