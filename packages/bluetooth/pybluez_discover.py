#!/usr/bin/env python
# --*--coding=utf-8--*--
# pip install pybluez

import time
from bluetooth import *


def ble_discover(n):
    """扫描蓝牙设备
    """
    for i in range(n):
        print(f'开始第 {i} 次扫描')
        foundDevs = discover_devices(lookup_names=True, lookup_class=True)
        for addr,name,_ in foundDevs:
            print(f"- 设备名称: {name}, MAC: {addr}")
        print()

if __name__ == "__main__":
    # 获取本机蓝牙地址
    ble_addr_local = read_local_bdaddr()
    print("本机蓝牙MAC地址:", ble_addr_local)

    ble_discover(1)