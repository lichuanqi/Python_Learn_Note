"""
3维曲面图
lichuan
lc@dlc618.com
"""
def xiaoshu_3(number):
    new = format(number, '.3f')

    return new


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np

 
x = np.linspace(9,10,100)
y = np.linspace(1,2.5,100)

X,Y = np.meshgrid(x,y)
# 图1
# Z1 = 4500000*(6*X**2-X*Y**2) / (4*X-Y**2)**2
# Z2 = 4500000*(2.16*X**2-X*Y**2) / (2.4*X-Y**2)**2
# Z3 = 4500000*X / (2*X-Y**2)

# 图2
Z1 = 3000 - 6000/(4*X - Y**2)
Z2 = 3000 - 6000/(2.4*X - Y**2)
Z3 = 3000 - 6000/(2*X - Y**2)

# 保存参数
filepath = '/media/lc/Data/modle_and_code/Python/2_Z3.txt'

# # 保存第1行表头
# txt_1 = 0
# for i in range(len(y)):
#     txt_1 = str(txt_1) +','+ xiaoshu_3(y[i])
# txt_1 = txt_1 +'\n'
# with open(filepath,'a+') as f:
#     f.write(str(txt_1))

# # 保存数据
# for i in range(len(x)):
#     # 输出的第i行
#     txt_i = xiaoshu_3(x[i])
#     for j in range(len(y)):
#         txt_i = txt_i +','+ xiaoshu_3(Z3[i][j])
#     txt_i = txt_i + '\n'
#     with open(filepath,'a+') as f:
#         f.write(str(txt_i))

# 画图

# 绘制三维曲面
fig = plt.figure()
ax=fig.add_subplot(111,projection='3d')
axes3d = Axes3D(fig)
axes3d.plot_surface(Y,X,Z1, rstride=1, cstride=1,cmap='binary')
axes3d.plot_surface(Y,X,Z2, rstride=1, cstride=1,cmap='binary')
axes3d.plot_surface(Y,X,Z3, rstride=1, cstride=1,cmap='binary')

ax.view_init(70, 60)

plt.savefig('/media/lc/Data/modle_and_code/Python/2_Z.png',dpi=200,bbox_inches='tight')
# plt.show()