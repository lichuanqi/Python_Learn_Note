"""
Detection callback w/ scanner
--------------
Example showing what is returned using the callback upon detection functionality
Updated on 2020-10-11 by bernstern <bernie@allthenticate.net>
"""
import time
import numpy as np
import argparse
import asyncio

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


SCAN_RESULT = {} # 扫描结果


def callback_scan(device: BLEDevice, advertisement_data: AdvertisementData):
    """扫描广播的回调函数"""
    address = device.address
    local_name = advertisement_data.local_name
    manufacturer_data = advertisement_data.manufacturer_data
    service_uuids = advertisement_data.service_uuids
    rssi = advertisement_data.rssi

    print("- %s: local_name=%r, rssi=%s"%(address, local_name, rssi))

    # 只保存有名称的
    if local_name:
        if address not in SCAN_RESULT:
            SCAN_RESULT[address] = {
                'local_name': local_name,
                'rssis': [],
            }

        SCAN_RESULT[address]['rssis'].append(rssi)


def callback_disconnected(client):
    print("Disconnected callback called!")


async def scan(services=None, macos_use_bdaddr=False):
    """扫描蓝牙设备
    扫描设备通过回调函数打印设备地址和广播数据
    通过 BleakScanner() 类实现

    Params
        services: UUIDs of one or more services to filter for
        macos_use_bdaddr: when true use Bluetooth address instead of UUID on macOS
    """
    services = ['00002a00-0000-1000-8000-00805f9b34fb']

    scanner = BleakScanner(
        detection_callback=callback_scan, 
        # service_uuids=services, 
        cb=dict(use_bdaddr=macos_use_bdaddr)
    )

    start_time = time.time()
    print('开始扫描: %s'%start_time)
    
    await scanner.start()
    await asyncio.sleep(5.0)
    await scanner.stop()

    end_time = time.time()
    print('扫描结束: %s'%end_time)

    for address,data in SCAN_RESULT.items():
        local_name = data['local_name']
        rssis = data['rssis']

        rssis_array = np.array(rssis)
        rssi_max = np.max(rssis_array)
        rssi_mean = np.mean(rssis_array)
        rssi_min = np.min(rssis_array)

        print(local_name)
        print('- address: %s'%address)
        print('- rssi_max: %s'%rssi_max)
        print('- rssi_mean: %.0f'%rssi_mean)
        print('- rssi_min: %s'%rssi_min)


async def scan_easy():
    """扫描蓝牙设备
    通过 BleakScanner.discover() 函数实现
    """
    print("scanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(
        timeout = 3,
        return_adv=True
    )

    for d, a in devices.values():
        print(d)
        print(a)
        print()


async def connect(address=None):
    """根据mac地址连接蓝牙设备
    
    Params
        address: 设备mac地址
    """
    address = '08:B6:1F:33:54:A6'
    services = ['0000181a-0000-1000-8000-00805f9b34fb']

    print("starting", address, "loop")
    async with BleakClient(address, 
                           disconnected_callback=callback_disconnected,
                           timeout=5.0
    ) as client:
        # 循环读取数据
        while client.is_connected:
            for service in client.services:
                print("[Service] %s", service)

                for char in service.characteristics:
                    if "read" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            print(
                                "  [Characteristic] %s (%s), Value: %r",
                                char,
                                ",".join(char.properties),
                                value,
                            )
                        except Exception as e:
                            print(
                                "  [Characteristic] %s (%s), Error: %s",
                                char,
                                ",".join(char.properties),
                                e,
                            )

                    else:
                        print(
                            "  [Characteristic] %s (%s)", char, ",".join(char.properties)
                        )

                    for descriptor in char.descriptors:
                        try:
                            value = await client.read_gatt_descriptor(descriptor.handle)
                            print("    [Descriptor] %s, Value: %r", descriptor, value)
                        except Exception as e:
                            print("    [Descriptor] %s, Error: %s", descriptor, e)


if __name__ == "__main__":
    asyncio.run(scan())