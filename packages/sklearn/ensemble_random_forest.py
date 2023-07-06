"""
集成学习 Ensemble Learning

在机器学习的有监督学习算法中，我们的目标是学习出一个稳定的且在各个方面表现都较好的模型，但实际情况往往不这么理想，
有时我们只能得到多个有偏好的模型（弱监督模型，在某些方面表现的比较好）。
集成学习就是组合这里的多个弱监督模型以期得到一个更好更全面的强监督模型，
集成学习潜在的思想是即便某一个弱分类器得到了错误的预测，其他的弱分类器也可以将错误纠正回来。
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn import datasets


# 加载糖尿病数据集
x,y = datasets.load_diabetes(return_X_y=True)


def test_random_forest():
    """随机森林回归 RandomForestRegressor
    
    随机森林是一种元估计器，它在数据集的不同子样本上匹配多个分类决策树，并使用均值来提高预测精度和控制过拟合。
    如果bootstrap=True(默认)，则使用max_samples参数控制子样本的大小，否则将使用整个数据集来构建每棵树。
    """
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # 训练和预测
    regressor = RandomForestRegressor(n_estimators=100, min_samples_leaf=5)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)

    # 计算真实结果与测试结果的拟合度
    print('sklearn score:{}'.format(r2_score(y_test, y_pred)))


if __name__ == "__main__":
    test_random_forest()