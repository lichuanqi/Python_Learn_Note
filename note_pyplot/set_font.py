"""
指定字体
lichuan
lc@dlc618.com
"""
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

# 读取字体
times = FontProperties(fname='/home/lcq/.local/share/fonts/Times New Roman/times.ttf', size=18)
heiti = FontProperties(fname='/home/lcq/.local/share/fonts/黑体/simhei.ttf', size=18)

# 标题字体
plt.title('Image Name',FontProperties=times)

# 坐标轴名称字体
plt.xlabel('Cow',FontProperties=times)
plt.ylabel('Col',FontProperties=times)

# 坐标轴刻度字体
plt.xticks(FontProperties=times)
plt.yticks(FontProperties=times)

plt.savefig('/media/lcq/Data/modle_and_code/data/test.jpg',dpi=300)
plt.show()