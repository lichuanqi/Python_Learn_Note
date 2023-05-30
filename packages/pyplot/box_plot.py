"""
箱线图

plt.boxplot(x,                      # x: 指定要绘制箱图的数据
            notch=None,           # notch: 是否是凹口的形式展现箱线图,默认非凹口
            sym=None,              # sym: 指定异常点的形状,默认为+号显示
            vert=None,              # vert: 是否需要将箱线图垂直摆放,默认垂直摆放
            whis=None,             # whis: 指定上下须与上下四分位的距离,默认为1.5倍的四分位差
            positions=None,   # positions: 指定箱线图的位置,默认为[0,1,2…]
            widths=None,         # widths: 指定箱线图的宽度,默认为0.5
            patch_artist=None,        # patch_artist: 是否填充箱体的颜色
            meanline=None,             # meanline: 是否用线的形式表示均值,默认用点来表示
            showmeans=None,       # showmeans: 是否显示均值,默认不显示
            showcaps=None,           # showcaps: 是否显示箱线图顶端和末端的两条线,默认显示
            showbox=None,             # showbox: 是否显示箱线图的箱体,默认显示
            showfliers=None,          # showfliers: 是否显示异常值,默认显示
            boxprops=None,           # boxprops: 设置箱体的属性,如边框色,填充色等
            labels=None,                  # labels: 为箱线图添加标签,类似于图例的作用
            flierprops=None,          # filerprops: 设置异常值的属性,如异常点的形状、大小、填充色等
            medianprops=None,   # medianprops: 设置中位数的属性,如线的类型、粗细等
            meanprops=None,       # meanprops: 设置均值的属性,如点的大小、颜色等
            capprops=None,           # capprops: 设置箱线图顶端和末端线条的属性,如颜色、粗细等
            whiskerprops=None)   # whiskerprops: 设置须的属性,如颜色、粗细、线的类型等
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 用来显示负号
plt.rcParams['savefig.dpi'] = 300

data = np.random.normal(size=(100, 10))
# print(data)

# 计算
for data_ in data:
    print(pd.DataFrame(data_).describe())

plt.figure()
plt.boxplot(data)
plt.xlabel("x")
plt.ylabel("y")
plt.minorticks_on()
plt.show()
plt.close()