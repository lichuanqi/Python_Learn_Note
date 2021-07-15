##################################
# 计算两点间距离的几种方法
# lichuan
# lc@dlc618.com
# 参考：https://www.jb51.net/article/164673.htm
##################################

import numpy as np

# 点
a = np.array([4,5])
b = np.array([1,1])

# 数据
a_list = np.array([[3,4],[4,5],[5,6]])

# 欧氏距离（L2范数）是最易于理解的一种距离计算方法，源自欧氏空间中两点间的距离公式。
op1=np.sqrt(np.sum(np.square(a-b)))
op2=np.linalg.norm(a-b)
print('欧式距离：%s'%(op2))

# 曼哈顿距离也称为城市街区距离
op4=np.linalg.norm(a-b,ord=1)
print('曼哈顿距离(城市街区距离)：%s'%(op4))

# 切比雪夫距离(Chebyshev Distance)
op5=np.abs(a-b).max()
op6=np.linalg.norm(a-b,ord=np.inf)
print('切比雪夫距离(Chebyshev Distance)：%s'%(op6))

# 夹角余弦(Cosine)
op7=np.dot(a,b)/(np.linalg.norm(a)*(np.linalg.norm(b)))
print('夹角余弦(Cosine)：%s'%(op7))


op10=np.linalg.norm(a_list,axis=1)
print('欧式距离：%s'%(op10))