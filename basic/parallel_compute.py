import multiprocessing
import os
import time


def run_case(*text):
    print('入参：{0}，当前进程号：{1}'.format(text, os.getpid()))
    time.sleep(1)


if __name__ == '__main__':
    pool_num = multiprocessing.Pool(3)
    print('主进程：{0}'.format(os.getpid()))
    print('子进程开始咯')
    for i in range(3):
        pool_num.apply_async(run_case, args=(i,))
    pool_num.close()
    pool_num.join()
    print('子进程结束了')
    print('主进程结束了')
