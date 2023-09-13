###################################
# 矩阵一一配对
# lichuan
# lc@dlc618.com
###################################

import numpy as np
import random as ra

x = [1,2,3,4,5]
y = [7,8,9,9,10]

xy = np.array([
    [1,2,3,4,5],
    [7,8,9,9,10]])
result = []

for i in range(len(x)):
    print([x[i],y[i]])

print(xy.shape)
for i in range(xy.shape[1]):
    for j in range(xy.shape[0]):
        print(i, j, xy[j, i])
print(xy[1,2])


x1 = np.arange(0, 15, 1)
x2 = np.linspace(0, 15, 15, endpoint=False)
print(x1)
print(x2)