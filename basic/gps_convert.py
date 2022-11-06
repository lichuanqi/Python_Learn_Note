#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import os
import math
 
 
pi = 3.14159265358979324
a = 6378245.0
ee = 0.00669342162296594323
x_pi = 3.14159265358979324 * 3000.0 / 180.0
 
 
def outOfChina(lat, lng):
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False
 
def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret
 
def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret
 
#地球坐标转换为火星坐标，即WGS84（国际通用）转为GCJ02坐标系适用于腾讯地图、高德（阿里）地图或谷歌地图
def WGS84toGCJ02(wgLat, wgLon):
    latlng = [1.0, 1.0]
    if outOfChina(wgLat, wgLon) == True:
        latlng[0] = wgLat
        latlng[1] = wgLon
        return latlng
 
    dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
    dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
    radLat = wgLat / 180.0 * pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * pi)
    latlng[0] = wgLat + dLat
    latlng[1] = wgLon + dLon
    return latlng
 
 
#地球坐标转换为百度坐标，即WGS84（国际通用）坐标系转为BD09坐标系适用于百度地图
def WGS84toBD09 (lat, lon):
    latlng = WGS84toGCJ02(lat, lon)
    x = latlng[1]
    y = latlng[0]
 
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    latlng[0] = z * math.sin(theta) + 0.006     #0.006     #0.01205
    latlng[1] = z * math.cos(theta) + 0.0062    #0.0065    #0.00370
    return latlng


if __name__=='__main__':

    lat = 31.23190588
    lng = 121.46952288
    print("WGS84: [%f,%f]" %(lng, lat))
    latlng = WGS84toGCJ02(lat, lng)
    print("GCJ02: [%f,%f]" %(latlng[1], latlng[0]))
    latlng = WGS84toBD09(lat, lng)
    print("BD09: [%f,%f]" %(latlng[1], latlng[0]))