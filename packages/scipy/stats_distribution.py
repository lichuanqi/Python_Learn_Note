from pprint import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from scipy.stats import pearsonr, spearmanr, kstest, anderson, uniform, norm
from scipy.stats import describe

matplotlib.use('TkAgg')


# np.random生成随机数
# x = np.random.uniform(low=5, high=10, size=2000)
x = np.random.normal(16, 7, 2000)

# scipy.stats生成随机数
# x = uniform.rvs(loc=0, scale=100, size=100, random_state=np.random.default_rng())
# x = norm.rvs(loc=0, scale=0.5, size=2000)


def data_viz():
    print(type(x))
    print(x)
    pprint(describe(x))

    # 散点图
    plt.subplot(1,2,1)
    plt.plot(x, 'o')
    
    # 频数直方图
    plt.subplot(1,2,2)
    count, bins, ignored = plt.hist(x, 15, density=True)
    plt.show()


def test_ks():
    # ks检验
    u, std = np.mean(x), np.std(x)
    sta, pvalue = kstest(x, norm.cdf, args=(u, std))
    print(sta, pvalue)


def test_anderson():
    """
    scipy.stats.anderson 检验正态分布

    该方法是由 scipy.stats.kstest 改进而来的，
    可以做正态分布、指数分布、Logistic 分布、Gumbel 分布等多种分布检验。
    默认参数为 norm 即正态性检验。

    input
        x - 待检验数据
        dist - 设置需要检验的分布类型

    output
        statistic - 统计数
        critical_values - 评判值
        significance_level - 显著性水平

        如果输出的统计量值statistic < critical_values
        则表示在相应的significance_level下
        接受原假设，认为样本数据来自给定的正态分布。
    """
    statistic, critical_values, significance_level = anderson(x, 'norm')
    print('statistic: %s\n, critical_values: %s\n, significance_level: %s\n'%(
        statistic, critical_values, significance_level))


data_viz()
# test_ks()
test_anderson()