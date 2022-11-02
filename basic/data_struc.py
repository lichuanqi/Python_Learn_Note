# python数据结构

from dataclasses import dataclass
from msilib.schema import Error
import re
from sqlite3 import DataError


def get_data_bytes(data):
    """
    根据微重力传感器传回的字节计算重量
    Arg
        data [bytes]: 微重力传感器传回的字节数据,如下格式
              \xbb\xbb\xbb\x01\xb1\x21\x34\x04\x03\x0b
    Return
        zhongliang [float]: 重量数值
        danwei [str]: 单位，['Mpa', 'Kg', 'T']
    """
    if not isinstance(data,bytes):
        raise BaseException('请检查数据类型是否为 bytes')

    dots = [1, 10, 100, 1000]
    danweis = ['Mpa', 'Kg', 'T']

    out_s = ''
    for i in range(0,len(data)):
        out_s = out_s + ' ' + str(data[i]) 
    out_s = out_s.strip().split(' ')

    h16 = '0x' + str(hex(int(out_s[5])))[2:] + str(hex(int(out_s[6])))[2:]
    print(f'h16: {h16}')
    data = int(h16, 16)
    xiaoshudian = dots[int(out_s[7])-1]
    zhongliang = data / xiaoshudian
    danwei = danweis[int(out_s[8])-1]
    
    return zhongliang, danwei

def test01():

    dots = [1, 10, 100, 1000]
    danweis = ['Mpa', 'Kg', 'T']

    h16 = '0x2134'
    dot = '0x04'
    danwei = '0x03'

    h16_10, dot_10,danwei_10 = int(h16, 16), int(dot,16), int(danwei,16)
    print(f'h16_10: {h16_10}, dot_10: {dot_10}, danwei_10: {danwei_10}')
    print(f'result: {h16_10/dots[dot_10-1]}({danweis[danwei_10-1]})')

def test02():

    a_en = b'\xbb\xbb\xbb\x01\xb1\x21\x34\x04\x03\x0b'
    print(f'data type: {type(a_en)}')

    a = a_en.hex()
    print(f'a: {a}')

if __name__ == '__main__':
    data = b'\xbb\xbb\xbb\x01\xb1\x00\x02\x04\x03\x0b'
    zl, dw = get_data_bytes(data)
    print(f'input: {data}')
    print(f'result: {zl} ({dw})')

    # test02()