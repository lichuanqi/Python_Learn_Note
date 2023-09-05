from pprint import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from scipy.stats import pearsonr, spearmanr, kstest, uniform, norm
from scipy.stats import describe

matplotlib.use('TkAgg')


x = [1.1,1,2.3,3,3,4,5,5,6,6]
y = [5,5,7,6.7,7,7.5,8,8,8,8]


def test_ks():
    # np.random生成随机数
    # x = np.random.uniform(low=5, high=10, size=20)
    # x = np.random.normal(0, 0.5, 200)

    # scipy.stats生成随机数
    # x = uniform.rvs(loc=0, scale=10, size=100, random_state=np.random.default_rng())
    x = norm.rvs(loc=0, scale=0.5, size=200)

    print(type(x))
    print(x)
    pprint(describe(x))

    # 频数直方图
    count, bins, ignored = plt.hist(x, 15, density=True)
    plt.show()

    # ks检验
    u, std = np.mean(x), np.std(x)
    sta, pvalue = kstest(x, norm.cdf, args=(u, std))
    print(sta, pvalue)


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


test_ks()
# test_pearsonr()
# test_spearmanr()