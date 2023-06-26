"""研究邮件重量与体积的相关性"""
import math
from pathlib import Path
import numpy as np
import pandas as pd 
from matplotlib import colors
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.neighbors import LocalOutlierFactor


def read_data_txt(txtfile):
    """从txt文档中读取重量体积数据
    
    Params
        txtfile: txt文件路径,数据保存格式如下
            1.3400,14.4370 
            4.1700,39.9230 
            1.6100,13.5050 
            2.4900,23.6430 
            ...

    Return
        x 所有的重量数据
        y 所有体积数据
    """
    x, y = [], []
    with open(txtfile) as f:
        for line in f.readlines():
            _x, _y = line.strip().split(',')
            x.append(float(_x))
            y.append(float(_y))
    
    return x,y


def run(x,y,savepath):
    # s
    savename_map = Path(savepath) / '0626_mat.jpg'
    savename_csv = Path(savepath) / '0626_mat.csv'

    # 数据区间
    xx = np.arange(0,11,1)
    # print(type(xx), xx)
    xx_headers = []
    for i in range(len(xx)):
        if i < len(xx)-1:
            xx_headers.append('%s-%s'%(xx[i], xx[i+1]))
        else:
            xx_headers.append('%s+'%(xx[i]))       
    print(xx_headers)

    yy = np.arange(0,101,4)
    # print(type(yy), yy)
    yy_headers = []
    for i in range(len(yy)):
        if i < len(yy)-1:
            yy_headers.append('%s-%s'%(yy[i], yy[i+1]))
        else:
            yy_headers.append('%s+'%(yy[i]))
    print(yy_headers)

    nums = np.zeros((len(xx),len(yy)))
    print(nums.shape)

    for _x,_y in zip(x,y):
        print('原始数据: %s,%s'%(_x,_y))
        
        # 确定行索引
        if _x > xx[-1]:
            _i = len(xx) - 1
        else:
            _i = math.floor(_x)
        
        # 确定列索引
        if _y > yy[-1]:
            _j = len(yy) - 1
        else:
            _j = int(_y) // 4

        print('计数矩阵索引号: %s,%s'%(_i, _j))
        nums[_i, _j] += 1


    print(nums)
    # 标准化
    nums_nor = normalize(nums, axis=1, norm='l1')

    # 绘制矩阵图
    plt.matshow(nums_nor, cmap=plt.cm.Reds)
    plt.title("matrix A")
    # plt.show()
    plt.savefig(savename_map,dpi=300, bbox_inches='tight')

    # 保存矩阵巍csv文件
    pd.DataFrame(nums_nor).to_csv(savename_csv, header=yy_headers)

def read_data_txt_test():
    x,y = read_data_txt('project/test/data_dws_hefei.txt')
    print('x len: %s, x len: %s'%(len(x), len(y)))


def hit():
    """直方图"""
    datapath = 'project/zhuangzailv/data_dws_hefei.txt'
    savedir = 'project/zhuangzailv'
    x, y = read_data_txt(datapath)
    data = np.vstack((np.array(x),np.array(y))).T

    # 筛选异常值
    clf = LocalOutlierFactor(n_neighbors=10)
    predict = clf.fit_predict(data)
    score = clf.negative_outlier_factor_

    # 绘制散点图
    # plt.scatter(x, y, s=20, c=predict, marker='o')
    # plt.show()

    # 重量体积二位直方图
    plt.hist2d(x, 
               y, 
               bins=10, 
               range=[[0, 15], [0, 80]], 
               weights=predict, 
               cmap='Blues',
               norm=colors.LogNorm())
    plt.colorbar()
    plt.show()


def run_test():
    # 原始数据
    x = [1.1,1,2.3,3,3,4,5,5,6,6]
    y = [5,5,7,6.7,7,7.5,8,8,8,8]
    savename = 'project/zhuangzailv/output.csv'
    run(x,y,savename)


def run_hefei():
    datapath = 'project/zhuangzailv/data_dws_hefei.txt'
    savedir = 'project/zhuangzailv'
    x, y = read_data_txt(datapath)
    run(x,y,savedir)


if __name__=="__main__":
    # read_data_txt_test()
    # run_hefei()
    hit()