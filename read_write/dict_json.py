"""字典数据与json文件之间的保存和读取
"""
import json

def dict2json(dicts:dict, savename:str) -> None:
    """字典保存为json文件
    Args
        dicts (dict)   : 要保存的字典数据
        savename (str) : 文件保存名称 *.json
    Output
        savename.json
    """
    with open(savename, "w", encoding='utf-8') as f:
        f.write(json.dumps(dicts, ensure_ascii=False, indent=4, separators=(',', ':')))


def json2dict(json_path) -> dict:
    """json文件读取为字典
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


if __name__=='__main__':

    data = {'1': '1频', '2': '2频'}
    savename = 'dataset/dict_json.json'

    # 保存
    dict2json(data, savename)

    # 读取
    data_read = json2dict(savename)
    print(data_read)