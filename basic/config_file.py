"""配置文件config"""
import json
from pathlib import Path
import configparser


class configIni():
    def __init__(self, cfgfile) -> None:
        self.cfgfile = cfgfile

        # TODO: 判断文件是否存在

        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.cfgfile)

        # 填充一些默认值
        self.cfg['DEFAULT'] = {'ServerAliveInterval': '45',
                               'Compression': 'yes',
                               'CompressionLevel': '9'}
        self.cfg['User'] = {'username': 'lichuan',
                            'passward': 'lichuan@123..'}

    def readValue(self, section, item):
        """读取item值"""
        return self.cfg[section][item]

    def setValue(self, section, item, value):
        """写入item值"""
        self.cfg.set(section, item, value)
        self.updateFile()

    def updateFile(self):
        with open(self.cfgfile, 'w') as configfile:
            self.cfg.write(configfile)


class configJson():
    def  __init__(self, cfgfile) -> None:
        self.cfgfile = cfgfile

        # TODO: 判断文件是否存在
        if Path(self.cfgfile).exists():
            self.readFile()
        else:
            self.cfg = {}

        # 填充一些默认值
        self.cfg['DEFAULT'] = {'ServerAliveInterval': '45',
                               'Compression': 'yes',
                               'CompressionLevel': '9'}
        self.cfg['User'] = {'username': 'lichuan',
                            'passward': 'lichuan@123..'}
    
    def readFile(self):
        """从文件读取配置参数"""
        with open(self.cfgfile, 'r', encoding='utf-8') as f:
            self.cfg = json.loads(f.read())

    def readValue(self, section, item):
        """读取item值"""
        return self.cfg[section][item]

    def setValue(self, section, item, value):
        """写入item值"""
        value_original = self.cfg[section][item]
        if value_original != value:
            self.cfg[section][item] = value
            self.updateFile()

    def updateFile(self):
        """修改参数后更新文件"""
        with open(self.cfgfile, 'w', encoding='utf-8') as f:
            json.dump(self.cfg, f, sort_keys=True, indent=4, ensure_ascii=False)


def test_config():
    # cfgfile = 'dataset/config.ini'
    # cfg = configIni(cfgfile)
    cfgfile = 'dataset/config.json'
    cfg = configJson(cfgfile)

    # 读取
    print(cfg.readValue('User', 'username'))

    # 写入
    cfg.setValue('User', 'passward', 'lcq')
    print(cfg.readValue('User', 'passward'))
    

if __name__ == '__main__':
    test_config()