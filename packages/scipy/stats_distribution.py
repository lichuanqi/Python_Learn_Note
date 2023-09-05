from pprint import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from scipy import stats
from scipy.stats import pearsonr, spearmanr, kstest, anderson, \
    skew, kurtosis, uniform, norm
from scipy.stats import describe

matplotlib.use('TkAgg')


# np.random生成随机数
x = np.random.uniform(low=5, high=5000, size=200)
# x = np.random.normal(16, 7, 2000)

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


def test_skew_kurtosis():
    """
    偏度-峰度检验

    标准正态分布偏度和峰度均为0。
    现实中的数据如果 |峰度|<10 && |偏度|<3,则说明数据虽然不是绝对正态,但基本可接受为正态分布。
    """
    skew = stats.skew(x)
    kurtosis = stats.kurtosis(x)
    print('偏度: %.4f, 峰度: %.4f'%(skew,kurtosis))


def test_ks():
    """
    ks检验

    Output
        sta 统计量,越接近0就越表明数据和标准正态分布拟合的越好
        pvalue P值大于显著性水平,通常是0.05,接受原假设,则判断样本的总体服从正态分布
    """
    u, std = np.mean(x), np.std(x)
    sta, pvalue = kstest(x, norm.cdf, args=(u, std))
    print('KS \nsta: %.4f, pvalue: %.4f'%(sta, pvalue))


def test_anderson():
    """
    scipy.stats.anderson 检验正态分布

    该方法是由 scipy.stats.kstest 改进而来的,
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
        接受原假设,认为样本数据来自给定的正态分布。
    """
    statistic, critical_values, significance_level = anderson(x, 'norm')
    print('anderson \nstatistic: %s\n critical_values: %s\n significance_level: %s\n'%(
        statistic, critical_values, significance_level))


data_viz()
test_skew_kurtosis()
test_ks()
test_anderson()