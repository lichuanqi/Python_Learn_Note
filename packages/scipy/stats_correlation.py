from pprint import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from scipy.stats import pearsonr, spearmanr, kstest, anderson, uniform, norm
from scipy.stats import describe

matplotlib.use('TkAgg')


# x = [1.1,1,2.3,3,3,4,5,5,6,6]
# y = [5,5,7,6.7,7,7.5,8,8,8,8]

# np.random生成随机数
x = np.random.uniform(low=5, high=10, size=2000)
y = np.random.normal(16, 7, 2000)


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


def test_pearsonr():
    """Pearson相关系数

    一种用于衡量两个变量之间线性关系的统计量
    值介于-1和1之间，其中-1表示完全负相关，0表示没有线性关系，1表示完全正相关。

    Return
        corr_coef
        p_value
    """
    corr_coef, p_value = pearsonr(x, y)
    print("pearsonr corr_coef: %s, p_value: %s"%(corr_coef, p_value))


def test_spearmanr():
    """Spearman等级相关系数
    
    一种用于衡量两个变量之间等级或有序关系的相关性指标
    它基于皮尔逊积矩相关系数的概念，但是使用等级而非连续变量来计算。
    
    Return
        corr_coef
        p_value
    """
    corr_coef, p_value = spearmanr(x, y)
    print("spearmanr corr_coef: %s, p_value: %s"%(corr_coef, p_value))


test_pearsonr()
# test_spearmanr()