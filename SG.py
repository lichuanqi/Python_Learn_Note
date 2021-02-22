"""
Savitzky-Golay滤波器用于曲线平滑
lichuan
lc@dlc618.com
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def SG_self():
    # SG from https://blog.csdn.net/qq_43790749/article/details/104970482
    arr = []
    window_size = 59
    k =3
    m = int((window_size-1)/2)
    for i in range(window_size):#如(2),(3)
        a = []
        for j in range(k):
            y_val = np.power(-m + i, j)
            a.append(y_val)
        arr.append(a)

    X = np.mat(arr)#X shape:(2m+1,k)
    print("变量矩阵x:",X)
    #print(arr.I)
    B = X * (X.T * X).I * X.T #如(6)#B shape:(2m+1,2m+1)
    print("矩阵 B:",B)
    # print(step)
    a = np.array(B[m])#只使用矩阵的第m行,a shape:(1,2m+1)
    print(a)
    a = a.reshape(window_size)
    print(a)
    #前后补齐,如(7)
    data = np.insert(data, 0, [data[0] for i in range(m)])
    data = np.append(data, [data[-1] for i in range(m)])
    print(data)
    list = []
    for i in range(m, data.shape[0] - m):
        arra = []
        for j in range(-m, m+1):
            arra.append(data[i +j])#找到临近的window_size个点,#arra shape:(1,2m+1)
        #print(arra)
        b = np.sum(np.array(arra) * a)#使用多项式求解,并把多项式结果作为平滑后的点,如(1),(5)
        # c = arr * (np.mat(arra).reshape(window_size,1))
        # for j in range(window_size):
        #     data[i - step + j] = c[j][0]
        # print(c.reshape(window_size))
        list.append(b)#得到所有平滑后的点
    print((list))

    return list


# generate a set of data randomly 
Size = 100
x = np.linspace(0,2*np.pi,100)
data = np.sin(x) + np.random.random(100) * 2
print("input data:",data)

# savgol_filter
y = savgol_filter(data, 59, 3, mode= 'nearest')

# plot
plt.figure(1)
plt.plot(x, data,color='y',label='pre_filter data')
plt.plot(x, y, 'b', label = 'savgol_filter')
# plt.plot(x, np.array(list), 'r', label = 'self')
plt.legend()
plt.savefig("sg.png",dpi=600)
plt.show()






