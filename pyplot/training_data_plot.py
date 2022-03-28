"""

Note: 根据训练数据绘制折线图

参考 https://blog.csdn.net/weixin_43748786/article/details/96434674

"""

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import csv

from pyparsing import alphas


def read_csv(csv_path):

	with open(csv_path,'r',encoding='utf-8') as f:
		csv_data = csv.reader(f)
		list_data = list(csv_data)

	# print(list_data[0][0])

	return list_data


def read_txt(path):
	with open(path, 'r') as f:
		lines = f.readlines()
	splitlines = [x.strip().split(' ') for x in lines]
	return splitlines


# Referenced from Tensorboard
# a smooth_loss function:https://blog.csdn.net/charel_chen/article/details/80364841)
def smooth_data(data, weight=0.1):
	
	last = data[0]
	smoothed = []
	for point in data:
		smoothed_val = last * weight + (1 - weight) * point
		smoothed.append(smoothed_val)
		last = smoothed_val

	return smoothed


if __name__ == "__main__":

	# 读取字体
	times = FontProperties(fname='C:/Windows/Fonts/Times New Roman/times.ttf', size=18)

	# Unet
	csv_path = "D:/Code/Keras-Semantic-Segmentation/expdata/0721_R660_unet/0721_R660_unetlog.csv"
	# Unet-1
	# csv_path = "D:/Code/Keras-Semantic-Segmentation/expdata/0721_R660_unet_1/0721_R660_1__nunetlog.csv"
	# Unet-2
	# csv_path = "D:/Code/Keras-Semantic-Segmentation/expdata/0721_R660_unet_2/0721_R660_2_nunetlog.csv"
	# Unet-3
	# csv_path = 'D:/Code/Keras-Semantic-Segmentation/expdata/0721_R660_unet_3/0721_R660_3_unetlog.csv'
	list_data = read_csv(csv_path)

	epoch = []
	acc = []
	loss = []
	val_acc = []
	val_loss = []

	print(len(list_data))

	for i in range(1,len(list_data)):

		epoch.append(int(list_data[i][0]))
		acc.append(float(list_data[i][1]))
		loss.append(float(list_data[i][3]))
		val_acc.append(float(list_data[i][7]))
		val_loss.append(float(list_data[i][9]))

	# smooth
	acc_smooth = smooth_data(acc)
	loss_smooth = smooth_data(loss)
	val_acc_smooth = smooth_data(val_acc)
	val_loss_smooth = smooth_data(val_loss)
	
	# print(epoch)
	# print(acc)
	# print(acc_smooth)
	
	# 准确率 Acc
	plt.figure()
	plt.plot(epoch,acc_smooth,label='train_acc')
	plt.plot(epoch,val_acc_smooth,label='val_acc')
	plt.ylim(0.88,1)
	# 坐标轴
	plt.xlabel('Epoch')
	plt.ylabel('Acc')
	# 坐标轴刻度字体
	plt.minorticks_on()
	plt.legend()
	plt.savefig('D:/论文/论文3-毕业论文/图片/图 22-Unet-1-准确率',dpi=300, bbox_inches='tight')

	# 损失函数 Loss
	plt.figure()
	plt.plot(epoch,loss_smooth,label='train_loss')
	plt.plot(epoch,val_loss_smooth,label='val_loss')
	# 坐标轴
	plt.xlabel('Epoch')
	plt.ylabel('Loss')
	# 坐标轴刻度字体
	plt.minorticks_on()
	plt.legend()
	plt.savefig('D:/论文/论文3-毕业论文/图片/图 22-Unet-2-损失函数',dpi=300, bbox_inches='tight')

	plt.show()