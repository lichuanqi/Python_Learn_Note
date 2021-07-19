# =======================================
# format 格式化输出
# lichuan
# lc@dlc618.com
# 2021.07.19
# =======================================

import time


# =============== 类型转换 ===============

# !s 相当于对于参数调用str()
print("He is {!s} years old.".format(26))
# !r 相当于对于参数调用repr()
print("He is a cute {!r}".format("boy"))


# =============== 多次填充 ===============

print('{0} multiplied by {1} is {0}'.format('a',1))


# ============= 按名称访问参数 =============

print('name: {last_name}{first_name}'.format(last_name='C.', first_name='L.'))
 
name= {'last_name': 'C.', 'first_name': 'L.'}
print('name: {last_name}{first_name}'.format(**name))


# ============= 通过参数的items访问 =============

list = ['L.C.', 'www.dlc618.com']
print("name:{0[0]}, web: {0[1]}".format(list))  # "0" 是必须的


# =============== 字符串对齐 ===============

# ^ | 居中,后面带宽度，
# < | 左对齐,后面带宽度，
# > | 右对齐,后面带宽度，
# : | 后面带填充的字符，只能是一个字符，不指定则默认是用空格填充

print('{:=<50}'.format(' left aligned '))
print('{:=>50}'.format(' right aligned '))
print('{:=^50}'.format(' centered '))


# =============== 截断字符串 ===============

print('截取前5个字符: {:.5}'.format('Hello C.L.'))


# =============== 数字格式化 ===============

print("保留两位小数: {:.2f}".format(3.1415926))
print('使用逗号作为千位分隔符: {:,}'.format(1234567890))
print('百分比: {:.2%}'.format(0.61898))


# =============== 时间格式化 ===============
time_now = time.time()
print('时间戳: {}'.format(time_now))
time_local = time.localtime(time_now)
print('时间元组: {}'.format(time_local))
time_str = time.strftime('%Y-%m-%d %H:%M:%S',time_local))
print('时间字符串: {}'.format(time_str)