from pprint import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from scipy.stats import pearsonr, spearmanr, kstest, anderson, uniform, norm
from scipy.stats import describe

matplotlib.use('TkAgg')


# x = np.array([1, 2, 3, 4, 5])
# y = np.array([5, 4, 3, 2, 1])

# total collagen (mg/g dry weight of liver)
x = np.array([7.1, 7.1, 7.2, 8.3, 9.4, 10.5, 11.4])
# free proline (μ mole/g dry weight of liver)
y = np.array([2.8, 2.9, 2.8, 2.6, 3.5, 4.6, 5.0])

# np.random生成随机数
# x = np.random.uniform(low=5, high=10, size=2000)
# x = np.random.normal(16, 7, 2000)
# y = np.random.normal(16, 7, 2000)


def data_viz():
    # 散点图
    plt.subplot(1,2,1)
    plt.plot(x, y, 'o')

    # 二维直方图
    plt.subplot(1,2,2)
    plt.hist2d(x, y, bins=20, density=True)
    plt.show()


def test_pearsonr():
    """Pearson相关系数

    一种用于衡量两个变量之间线性关系的统计量

    Return
        corr_coef 相关系数 [-1,1]之间
            -1表示完全负相关,0表示没有线性关系,1表示完全正相关。
        p_value p值越小,表示相关系数越显著,一般p值在500个样本以上时有较高的可靠性。
    """
    corr_coef, p_value = pearsonr(x, y)
    print("pearsonr corr_coef: %.4f, p_value: %.4e"%(corr_coef, p_value))


def test_spearmanr():
    """Spearman等级相关系数
    
    一种用于衡量两个变量之间等级或有序关系的相关性指标
    它基于皮尔逊积矩相关系数的概念,但是使用等级而非连续变量来计算。
    
    Params
    ------
        

    Return
    ------
        corr_coef
        p_value
    """
    corr_coef, p_value = spearmanr(x, y)
    print("spearmanr corr_coef: %.4f, p_value: %.4e"%(corr_coef, p_value))


data_viz()
test_pearsonr()
test_spearmanr()