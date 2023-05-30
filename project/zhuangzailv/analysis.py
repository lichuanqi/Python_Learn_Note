"""
根据车管平台已发运邮路信息分析各吨位车型车厢容积的区间
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 用来显示负号
plt.rcParams['savefig.dpi'] = 300


def get_boxplot_data(data):
    """计算箱线图的数据"""

    # 排序
    data = sorted(data)

    # 中位数
    mid = np.median(data)
    
    # 均值
    mean = np.mean(data)

    # 上下四分位数
    q1 = np.quantile(data,0.25,interpolation='lower')
    q3 = np.quantile(data,0.75,interpolation='lower')
    iqr = q3 - q1
    
    # 上下边缘
    q4 = q1 - 0.5*iqr
    q5 = q3 + 0.5*iqr

    return q1, mid, q3, q4, q5, mean


def test_get_boxplot_data():

    data = [1,2,3,4,5]
    q1, mid, q3, q4, q5, mean = get_boxplot_data(data)
    print('--', q1, mid, q3, q4, q5)
    print('--中位数: %s'%(mid))
    print('--均值: %s'%(mean))
    print('--上下四分位区间: [%s, %s]'%(q1, q3))
    print('--上下边缘区间: [%s, %s]'%(q4, q5))


    plt.figure()
    plt.title('各吨位车厢容积分布')
    plt.boxplot(data,
                whis=1.5,
                showmeans=True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.minorticks_on()
    plt.show()

def main():
    data_file = "D:/CPRI/项目-邮件装载率/数据/已发运邮路信息-车管平台-重庆中心-精简.xlsx"
    data = pd.read_excel(data_file)
    print('数据读取完成')

    # 列标题
    print('columns:', data.columns)

    # 统计各吨位的容积
    data_analysis = {}
    for index,row in data.iterrows():

        # if index >= 100:
        #     break

        dunwei = int(row['车辆折算载重量1'])
        rongji = int(row['车辆容积(m³)'])

        if dunwei not in data_analysis.keys():
            data_analysis[dunwei] = []
        data_analysis[dunwei].append(rongji)

    # 按照key排序
    data_analysis_s = dict(sorted(data_analysis.items(), key=lambda k: k[0]))
    # print(data_analysis_s)

    # 转换为array
    plot_labels = []
    plot_data = []
    for key,value in data_analysis_s.items():
        if len(value) >= 10:
            print('吨位: %s, 数据量: %s'%(key, len(value)))
            plot_labels.append(key)
            plot_data.append(np.array(value))

            # 计算数据
            q1, mid, q3, q4, q5, mean = get_boxplot_data(value)
            print('--', q1, mid, q3, q4, q5)
            print('--中位数: %s'%(mid))
            print('--均值: %s'%(mean))
            print('--上下四分位区间: [%s, %s]'%(q1, q3))
            print('--上下边缘区间: [%s, %s]'%(q4, q5))
        
        else:
            print('吨位: %s, 数据量: %s, 已跳过'%(key, len(value)))

    plot_data = np.array(plot_data)
    # print(plot_data)

    # 画图
    plt.figure()
    plt.title('各吨位车厢容积分布')
    rsl = plt.boxplot(plot_data,
                    whis=1.5,
                    labels=plot_labels,
                    showmeans=True)
    plt.xlabel("吨位")
    plt.ylabel("容积")
    plt.minorticks_on()
    plt.savefig('project/zhuangzailv/save.jpg')
    plt.show()


if __name__ == "__main__":
    test_get_boxplot_data()