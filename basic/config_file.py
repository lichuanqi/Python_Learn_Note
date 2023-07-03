"""配置文件config"""
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
        # self.cfg[section][item] = value
        self.cfg.set(section, item, value)

        with open(self.cfgfile, 'w') as configfile:
            self.cfg.write(configfile)


class configJson():
    def  __init__(self) -> None:
        pass



def test_config():
    cfgfile = 'dataset/config.ini'
    cfg = configIni(cfgfile)

    # 读取
    print(cfg.readValue('User', 'username'))

    # 写入
    cfg.setValue('User', 'passward', 'lcq')
    print(cfg.readValue('User', 'passward'))
    

if __name__ == '__main__':
    test_config()