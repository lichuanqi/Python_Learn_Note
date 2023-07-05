import numpy as np
from scipy.stats import pearsonr, spearmanr

x = [1.1,1,2.3,3,3,4,5,5,6,6]
y = [5,5,7,6.7,7,7.5,8,8,8,8]


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
test_spearmanr()