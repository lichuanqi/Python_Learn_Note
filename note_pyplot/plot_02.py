"""
气泡图
lichuan
lc@dlc618.com
"""
import matplotlib.pyplot as plt
import numpy as np


names = ['Frame Difference', 'GMM', 'YOlO v3', 'This paper']
x = [0.285,0.272,0.893,0.898]                 # precision
y = [0.991,0.999,0.913,0.942]                 # recall
z = np.array([25,43,577,21])                  # time
c = np.array([0.1, 0.3, 0.6, 0.9]) * 10       # color

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, z*20, c, alpha=0.6)
plt.xlabel('Precision', fontsize=14)
plt.ylabel('Recall', fontsize=14)
# time图例
handles_01, labels_01 = scatter.legend_elements(prop='sizes')
legend1 = ax.legend(handles_01, sorted(z), loc=1, title="Time (s)", fontsize=11)
ax.add_artist(legend1)
# 算法图例
handles_02, labels_02 = scatter.legend_elements(prop='colors')
print(handles_02)
legend2 = ax.legend(handles_02, names, loc=3, title="Algorithm", fontsize=11)

plt.show()