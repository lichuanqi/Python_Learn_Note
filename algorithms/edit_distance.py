"""计算中文字符串编辑距离"""
import time
import numpy as np


def zh_Levenshtein_Distance_Recursive(str1, str2):
 
    if len(str1) == 0:
        return len(str2)
    elif len(str2) == 0:
        return len(str1)
    elif str1 == str2:
        return 0
 
    if str1[len(str1)-1] == str2[len(str2)-1]:
        d = 0
    else:
        d = 1

    distance = min(zh_Levenshtein_Distance_Recursive(str1, str2[:-1]) + 1, 
                   zh_Levenshtein_Distance_Recursive(str1[:-1], str2) + 1, 
                   zh_Levenshtein_Distance_Recursive(str1[:-1], str2[:-1]) + d)
    
    return distance
 

def zh_Levenshtein_Distance(str1, str2):
    """计算字符串 str1 和 str2 的编辑距离
    :param str1
    :param str2
    :return:
    """
    matrix = [[ i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
 
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            if(str1[i-1] == str2[j-1]):
                d = 0
            else:
                d = 1
            
            matrix[i][j] = min(matrix[i-1][j]+1, matrix[i][j-1]+1, matrix[i-1][j-1]+d)
 
    return matrix[len(str1)][len(str2)]
 

def _levenshtein_distance(ref, hyp):
    """Levenshtein distance is a string metric for measuring the difference
    between two sequences. Informally, the levenshtein disctance is defined as
    the minimum number of single-character edits (substitutions, insertions or
    deletions) required to change one word into the other. We can naturally
    extend the edits to word level when calculate levenshtein disctance for
    two sentences.
    """
    m = len(ref)
    n = len(hyp)

    # special case
    if ref == hyp:
        return 0
    if m == 0:
        return n
    if n == 0:
        return m

    if m < n:
        ref, hyp = hyp, ref
        m, n = n, m

    # use O(min(m, n)) space
    distance = np.zeros((2, n + 1), dtype=np.int32)

    # initialize distance matrix
    for j in range(n + 1):
        distance[0][j] = j

    # calculate levenshtein distance
    for i in range(1, m + 1):
        prev_row_idx = (i - 1) % 2
        cur_row_idx = i % 2
        distance[cur_row_idx][0] = i
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                distance[cur_row_idx][j] = distance[prev_row_idx][j - 1]
            else:
                s_num = distance[prev_row_idx][j - 1] + 1
                i_num = distance[cur_row_idx][j - 1] + 1
                d_num = distance[prev_row_idx][j] + 1
                distance[cur_row_idx][j] = min(s_num, i_num, d_num)

    return distance[m % 2][n]


str1 = "中共"
str2 = "中共中央"

ts = time.time()
for i in range(10000):
    zh_Levenshtein_Distance_Recursive(str1, str2)
te = time.time()
print('time used: %s'%(te-ts))

ts = time.time()
for i in range(10000):
    zh_Levenshtein_Distance(str1, str2)
te = time.time()
print('time used: %s'%(te-ts))

ts = time.time()
for i in range(10000):
    _levenshtein_distance(str1, str2)
te = time.time()
print('time used: %s'%(te-ts))