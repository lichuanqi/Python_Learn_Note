"""字典dict与yaml文件之间的保存和读取"""
import yaml


def dict2yaml(dicts:dict, savename:str) -> None:
    """字典保存为yaml文件
    Args
        dicts (dict)   : 要保存的字典数据
        savename (str) : 文件保存名称
    Output
        savename.yaml
    """
    with open(savename, 'w', encoding='utf-8') as f:
        f.write(yaml.dump(dicts, allow_unicode=True))


def yaml2dict(savename:str) -> dict:
    """yaml文件读取为字典"""
    with open(savename, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)

    return data


if __name__=='__main__':

    data = {'1': {'速递': '11'}, '2': '2频'}
    savename = 'dataset/dict_yaml.yaml'
    
    # 保存
    dict2yaml(data, savename)

    # 读取
    data = yaml2dict(savename)
    print(data)