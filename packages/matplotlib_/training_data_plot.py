"""

Note: 根据训练数据绘制折线图

参考 https://blog.csdn.net/weixin_43748786/article/details/96434674

"""

import re
from trace import Trace
import numpy as np
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


def plot_keras_data():

	# Unet
	# csv_path = "D:/Code/Keras-Semantic-Segmentation/expdata/0721_R660_unet/0721_R660_unetlog.csv"
	# Unet-1
	# csv_path = "D:/Code/Keras-Semantic-Segmentation/expdata/0721_R660_unet_1/0721_R660_1__nunetlog.csv"
	# Unet-2
	# csv_path = "D:/Code/Keras-Semantic-Segmentation/expdata/0721_R660_unet_2/0721_R660_2_nunetlog.csv"
	# Unet-3
	# csv_path = 'D:/Code/Keras-Semantic-Segmentation/expdata/0721_R660_unet_3/0721_R660_3_unetlog.csv'
	
	
	# 0328版 - unet
	# csv_path = "D:/Code/Keras-Semantic-Segmentation/expdata/20220328_R660_unet/log.csv"
	# 0328版 - nunet
	csv_path = "D:/Code/Keras-Semantic-Segmentation/expdata/20220328-R660x9_nunet/log.csv"

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
	# plt.savefig('D:/论文/论文3-毕业论文/图片/图 22-Unet-1-准确率',dpi=300, bbox_inches='tight')

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
	# plt.savefig('D:/论文/论文3-毕业论文/图片/图 22-Unet-2-损失函数',dpi=300, bbox_inches='tight')

	plt.show()

	return True


def plot_yolov5_data(is_save=False):

	csv_path = "D:/Code/Pytorch-YOLOV5/runs/train-20220330-yolov5-Rail14/log.csv"

	list_data = read_csv(csv_path)

	epoch = []
	train_prcision = []
	train_recall = []
	train_loss_total = []
	val_loss_total = []
	map05 = []
	map0595 = [] 

	for i in range(0,len(list_data)):

		epoch.append(int(list_data[i][0]))
		train_prcision.append(float(list_data[i][8]))
		train_recall.append(float(list_data[i][9]))
		train_loss_total.append(float(list_data[i][5]))
		val_loss_total.append(float(list_data[i][15]))
		map05.append(float(list_data[i][10]))
		map0595.append(float(list_data[i][11]))
		
	# smooth
	train_prcision = smooth_data(train_prcision,weight=0.7)
	train_recall = smooth_data(train_recall,weight=0.5)
	# train_loss_total = smooth_data(train_loss_total,weight=0.5)
	# val_loss_total = smooth_data(val_loss_total,weight=0.5)
	map05 = smooth_data(map05,weight=0.5)
	map0595 = smooth_data(map0595,weight=0.5)

	# train_prcision
	plt.figure()
	plt.plot(epoch,train_prcision,label='prcision')
	# plt.ylim(0.88,1)
	# 坐标轴
	plt.xlabel('Epoch')
	plt.ylabel('Prcision')
	# 坐标轴刻度字体
	plt.minorticks_on()
	plt.legend()
	if is_save:
		plt.savefig('D:/论文/论文3-毕业论文/图片/图 43-1-precison.jpg',dpi=300, bbox_inches='tight')
	
	# racall
	plt.figure()
	plt.plot(epoch,train_recall,label='recall')
	# plt.ylim(0.88,1)
	# 坐标轴
	plt.xlabel('Epoch')
	plt.ylabel('Recall')
	# 坐标轴刻度字体
	plt.minorticks_on()
	plt.legend()
	if is_save:
		plt.savefig('D:/论文/论文3-毕业论文/图片/图 43-2-recall.jpg',dpi=300, bbox_inches='tight')
	
	# loss
	fig2 = plt.figure()
	plt.plot(epoch,train_loss_total,label='train_loss')
	plt.plot(epoch,val_loss_total,label='val_loss')
	# plt.ylim(0.88,1)
	# 坐标轴
	plt.xlabel('Epoch')
	plt.ylabel('Loss')
	# 坐标轴刻度字体
	plt.minorticks_on()
	plt.legend()
	if is_save:
		plt.savefig('D:/论文/论文3-毕业论文/图片/图 43-3-loss.jpg',dpi=300, bbox_inches='tight')

	# map
	plt.figure()
	plt.plot(epoch,map05,label='map05')
	# plt.ylim(0.88,1)
	# 坐标轴
	plt.xlabel('Epoch')
	plt.ylabel('mAP')
	# 坐标轴刻度字体
	plt.minorticks_on()
	plt.legend()
	if is_save:
		plt.savefig('D:/论文/论文3-毕业论文/图片/图 43-4-map05.jpg',dpi=300, bbox_inches='tight')
	
	# map 0595	 
	plt.figure()
	plt.plot(epoch,map0595,label='map0595')
	# plt.ylim(0.88,1)
	# 坐标轴
	plt.xlabel('Epoch')
	plt.ylabel('mAP')
	# 坐标轴刻度字体
	plt.minorticks_on()
	plt.legend()
	if is_save:
		plt.savefig('D:/论文/论文3-毕业论文/图片/图 43-5-map0595.jpg',dpi=300, bbox_inches='tight')

	plt.show()

	return True


if __name__ == "__main__":

	# plot_keras_data()
	plot_yolov5_data(is_save=True)