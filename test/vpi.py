# 蒙特卡罗方法计算圆周率
# lichuan
# lc@dlc618.com

import random


def getPi(N):
        cnt = 0
        for i in range(N) :
            x = random.uniform(0,1)
            y = random.uniform(0,1)
            
            if (x*x + y*y) < 1 :
                cnt += 1
        vPi = 4.0 * cnt / N
        return vPi
 

print(getPi(10000))
