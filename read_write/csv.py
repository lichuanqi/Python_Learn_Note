###################################################
# csv 文件是一种逗号分隔的纯文本形式存储的表格数据
# Python内置了CSV模块，可直接通过该模块实现csv文件的读写操作
# 在web应用中导出数据是比较常见操作。
# @lichuan
# @lc@dlc618.com
###################################################

import csv

def csv_write():
    """
    @ 写操作
    @ writer.writerow， 将多列数据写入一行
    @ 如果以文本文件的方式打开，每行数据之间都是用逗号隔开的文本字符串
    @ 写入时，必须指定 newline=’’， 否则每插入一行就有一个空行
    """

    with open('note_basic/example.csv', 'w', newline='') as f: 
        writer = csv.writer(f)
        writer.writerow(["123", "234", "345"])
        writer.writerow(["abc", "efg", "hij"])


def csv_write_header():
    """
    @ 表头
    """
    fieldnames = ["name", "age", "sex"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"name": "zhangsan", "age": 10, "sex": "male"})
    writer.writerow({"name": "lis", "age": 20, "sex": "male"})


def csv_read():
    """
    @ 读操作
    """
    with open('note_basic/example.csv', 'r', newline="") as f: 
        reader = csv.reader(f)
        for row in reader:
            print(row)


def csv_write_dict():
    """
    @ 每行输出的是一个字典对象
    """
    with open('person.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)


if __name__ == '__main__':
    csv_write()
    print('写入成功')

    print('输出：')
    csv_read()
