"""
气泡图
lichuan
lc@dlc618.com
"""
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


# 读取字体
times = FontProperties(fname='/home/lcq/.local/share/fonts/Times New Roman/times.ttf', size=18)

names = ['FD', 'GMM', 'YOlO v3', 'This paper']
x = [0.285,0.272,0.893,0.898]                 # precision
y = np.array([0.991,0.999,0.913,0.942])       # recall
z = np.array([0.033,0.057,0.769,0.028])       # time
c = np.array([0.1, 0.3, 0.6, 0.9])            # color

m = np.array([0.443,0.428,0.903,0.919])       # F1
n = np.array([0.285,0.272,0.823,0.851])       # Similarity

legend_no = ['0.05','0.10','0.15','0.20']

# Precision, Recall, and Time
# fig, ax = plt.subplots()
# scatter = ax.scatter(x, y, z*6000, c, alpha=0.6)
# # 坐标轴
# plt.xlabel('Precision (%)', FontProperties=times)
# plt.ylabel('Recall (%)', FontProperties=times)
# # 坐标轴刻度字体
# plt.xticks(FontProperties=times)
# plt.yticks(FontProperties=times)
# plt.xlim(0, 1)
# plt.ylim(0.9, 1.01)
# plt.minorticks_on()
# # Time图例
# handles_01, labels_01 = scatter.legend_elements(prop='sizes', alpha=0.6, num=4)
# legend1 = ax.legend(handles_01, legend_no, loc=2, title="Time (s)", fontsize=11,markerscale=0.3,borderpad=1,labelspacing=1)
# ax.add_artist(legend1)
# # 算法图例
# handles_02, labels_02 = scatter.legend_elements(prop='colors', alpha=0.6)
# legend2 = ax.legend(handles_02, names, loc=3, title="Method", fontsize=11, markerscale=1.6)

# plt.savefig('/media/lcq/Data/modle_and_code/data/paper1-analysis/Precision-Recall-Time-2.jpg',dpi=300, bbox_inches='tight')


# F1, Similarity, and Time
fig, ax = plt.subplots()
scatter = ax.scatter(m, n, z*6000, c, alpha=0.6, marker='*')
# 坐标轴
plt.xlabel('F1(%)', FontProperties=times)
plt.ylabel('Similarity(%)', FontProperties=times)
# 坐标轴刻度字体
plt.xticks(FontProperties=times)
plt.yticks(FontProperties=times)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.minorticks_on()
# Time图例
handles_01, labels_01 = scatter.legend_elements(prop='sizes', alpha=0.6, num=4)
legend1 = ax.legend(handles_01, legend_no, loc=2, title="Time (s)", fontsize=12,markerscale=0.3,borderpad=1,labelspacing=1)
ax.add_artist(legend1)
# 算法图例
handles_02, labels_02 = scatter.legend_elements(prop='colors', alpha=0.6)
legend2 = ax.legend(handles_02, names, loc=3, title="Method", fontsize=12, markerscale=1.6)
plt.savefig('/media/lcq/Data/modle_and_code/data/paper1-analysis/F1-Similarity-Time-2.jpg',dpi=300, bbox_inches='tight')

plt.show()