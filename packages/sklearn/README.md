# 最近邻 `neighbors.py`

最近邻是从训练样本中找到与新点在距离上最近的预定数量的几个点。


# 离群点检测 `outlier_detection.py` 

离群点检测是指训练数据包含离群点,即远离其它内围点。离群点检测估计器会尝试拟合出训练数据中内围点聚集的区域, 会忽略有偏离的观测值。

常用的检测方法有：

## 椭圆模型拟合 Fitting an elliptic envelope

实现离群点检测的一种常见方式是假设常规数据来自已知分布（例如，数据服从高斯分布）。 从这个假设来看，我们通常试图定义数据的 “形状”，并且可以将偏远观测(outlying observation)定义为足够远离拟合形状的观测。`covariance.EllipticEnvelope`能拟合出数据的稳健协方差估计，从而为中心数据点拟合出一个椭圆，忽略不和该中心模式相关的点

## 隔离森林 Isolation Forest

在高维数据集中实现离群点检测的一种有效方法是使用随机森林。`ensemble.IsolationForest` 通过随机选择一个特征,然后随机选择所选特征的最大值和最小值之间的分割值来"隔离"观测。

```python
from sklearn.ensemble import # 2.7.4Forest
import numpy as np

X = np.array([[-1, -1], [-2, -1], [-3, -2], [0, 0], [-20, 50], [3, 5]])
clf = IsolationForest(n_estimators=10, warm_start=True)
clf.fit(X)  # fit 10 trees  
clf.set_params(n_estimators=20)  # add 10 more trees  
clf.fit(X)  # fit the added trees  
```

## 局部离群因子（LOF）

LOF是基于密度的经典算法，在 LOF 之前的异常检测算法大多是基于统计方法的，或者是借用了一些聚类算法用于异常点的识别，如DBSCAN，OPTICS。这些方法都有一些不完美的地方，比如基于统计的方法需要假设数据服从特定的概率分布，聚类方法通常只能给出是否为异常点的判别，不能量化每个数据点的异常程度。

首先，基于密度的离群点检测方法有一个基本假设：非离群点对象周围的密度与其邻域周围的密度类似，而离群点对象周围的密度显著不同于其邻域周围的密度。

计算的基本流程如下：
1. 对于每个数据点，计算它与其他数据点的距离，并按照由近到远排序
2. 对于每个数据点，找到它的k近邻的点，计算LOF得分
3. 如果LOF值越大说明越异常，反之则正常

考虑的k个近邻数（别名参数 n_neighbors ）通常选择 1) 大于一个聚类簇必须包含对象的最小数量，以便其它对象可以成为该聚类簇的局部离散点，并且 2) 小于可能成为聚类簇对象的最大数量, 减少这K个近邻成为离群点的可能性。在实践中，这样的信息通常不可用，并且使 n_neighbors = 20 似乎通常都能使得算法有很好的表现。 当离群点的比例较高时（即大于 10% 时，如下面的示例），n_neighbors 应该较大（在下面的示例中，n_neighbors = 35）。

当使用 LOF 进行离群点检测的时候，不能使用 `predict`, `decision_function` 和 `score_samples` 方法， 只能使用 `fit_predict` 方法。训练样本的异常性得分可以通过 `negative_outlier_factor_` 属性来获得。 注意当使用LOF算法进行新奇点检测的时候(参数`novelty`=True)， `predict`, `decision_function` 和 `score_samples` 函数可被用于新的未见过数据。

# 新奇点检测 `TODO`

新奇点检测是指训练数据未被离群点污染，我们对新观测值是否为离群点感兴趣。在这个语境下，离群点被认为是新奇点。