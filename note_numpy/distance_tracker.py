##################################
# 计算两个轨迹向量距离的几种方法
# lichuan
# lc@dlc618.com
# 参考：https://blog.csdn.net/u011333734/article/details/80930600?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-19.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-19.control
##################################

import numpy as np
from math import radians, cos, sin, atan2, sqrt


def lcss(s, t):
    len_s = len(s)
    len_t = len(t)
    pref_matrix = [[] for i in range(0, len_s)]
    maxlen = 0
    maxstr = []
    for i in range(0, len_s):
        s_i = s[i]
        for j in range(0, len_t):
            t_j = t[j]
            if s_i == t_j:
                if (i == 0) or (j == 0):
                    pref_matrix[i].append(1)
                else:
                    pref_matrix[i].append(pref_matrix[i-1][j-1] + 1)
                if pref_matrix[i][j] > maxlen:
                    maxlen = pref_matrix[i][j]
                    substr = s[(i+1)-maxlen:(i+1)]
                    maxstr = [substr]
                elif pref_matrix[i][j] == maxlen:
                    substr = s[(i+1)-maxlen:(i+1)]
                    if substr not in maxstr:
                        maxstr.append(substr)
            else:
                pref_matrix[i].append(0)
    return maxstr


def lcs(a, b):
    lena = len(a)
    lenb = len(b)
    c = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
    flag = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
    for i in range(lena):
        for j in range(lenb):
            if a[i] == b[j]:
                c[i + 1][j + 1] = c[i][j] + 1
                flag[i + 1][j + 1] = 'ok'
            elif c[i + 1][j] > c[i][j + 1]:
                c[i + 1][j + 1] = c[i + 1][j]
                flag[i + 1][j + 1] = 'left'
            else:
                c[i + 1][j + 1] = c[i][j + 1]
                flag[i + 1][j + 1] = 'up'
    return c, flag


def printLcs(flag, a, i, j):

    if i == 0 or j == 0:
        return
    if flag[i][j] == 'ok':
        printLcs(flag, a, i - 1, j - 1)
        # print a[i - 1]
        li.append(a[i-1])
    elif flag[i][j] == 'left':
        printLcs(flag, a, i, j - 1)
    else:
        printLcs(flag, a, i - 1, j)

    return li


# 给定两个轨迹
a = np.array([180, 180, 141, 146, 141, 200, 235, 235, 173, 141, 141, 172, 180])
b = np.array([165, 235, 180, 141, 240, 171, 173, 172])

# 给定两个轨迹 - 1-D的距离
a2 = np.array([4,5,4,5,6,4,5])
b2 = np.array([1,3,2,3,2,4,2])

# CDP
# 即找出两条轨迹之间两点距离最近的两个点，以该点对的距离作为轨迹距离。
# 定义简单，但是容易受到局部极端情况的影响，考虑两条轨迹在某点相交，
# 然而整体情况差异很大，这种情况用CPD距离显然不合适。总体来说，这种方法不是很好。
CDPab = np.min(np.abs(a2-b2))
print('SDP 距离：%s' % (CDPab))

# SDP
# 对两条轨迹对应序号的点对计算距离并求和，以该求和距离作为轨迹相似性分数。
# 要求轨迹A和轨迹B具有相同的轨迹点个数


# LCSS
# a、b表示两个mac在某段时间内的轨迹id序列
li =[]
c, flag = lcs(a, b)
li = printLcs(flag, a, len(a), len(b))
print ('LCSS 最长子系列：%s'%li)
print ('LCSS 最长子系列长度：%s'%len(li))
LCSSab = len(li)/min(len(a),len(b))
print('LCSS 相似度归一化结果：%s' % (LCSSab))

# DTW


# EDR


# H


# O
