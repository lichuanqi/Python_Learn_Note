"""列表与txt文件之间的保存和读取"""


def list2txt(data:list, savename:str) -> None:
    """列表保存为txt文件
    Params
        data     : 要保存的列表数据
        savename : 保存文件名称
    Output
        savename.txt
    """
    with open(savename, 'w', encoding='utf-8') as f:
        for _data in data:
            if isinstance(_data, list):
                data_write = ','.join(_data) + '\n'
                f.write(data_write)
            else:
                f.write(_data)


def txt2list(savename:str) -> list:
    """
    Params
        savename : 文件名称
    Return
        data
    """
    data = []
    with open(savename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            data.append(line.strip())

    return data


if __name__ == "__main__":

    data = [['日期', '方案', '总相对投递范围', ' 均相对投递范围'],
            ['20220808', 'A', '2.5', '0.6']]
    savename = 'dataset/list_txt.txt'

    # 保存
    list2txt(data, savename)

    # 读取
    data_read = txt2list(savename)
    print(data_read)