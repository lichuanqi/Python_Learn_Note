########################################
# array数据的保存和读取
# lichuan
# lc@dlc618.com
########################################

import numpy as np


data = [[1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0], [4, 0, 0, 0, 0], [5, 0, 0, 0, 0]]

# 保存
np.savetxt('array_data.txt', data)

# 读取
data_load = np.loadtxt('array_data.txt')
print(data_load[:,0])