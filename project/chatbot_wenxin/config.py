import datetime
import json
from json import JSONEncoder
from pathlib import Path


class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


class ConfigJson():
    def  __init__(self, cfgfile) -> None:
        self.cfgfile = cfgfile

        # TODO: 判断文件是否存在
        if Path(self.cfgfile).exists():
            self.readFile()
        else:
            self.cfg = {}
    
    def readFile(self):
        """从文件读取配置参数"""
        with open(self.cfgfile, 'r', encoding='utf-8') as f:
            self.cfg = json.loads(f.read())

    def readValue(self, section, item):
        """读取item值"""
        try:
            return self.cfg[section][item]
        except KeyError:
            return 'novlaue'

    def setValue(self, section, item, value):
        """写入item值"""
        value_original = self.readValue(section, item)
        if value_original != value:
            self.cfg[section][item] = value
            self.updateFile()

    def updateFile(self):
        """修改参数后更新文件"""
        with open(self.cfgfile, 'w', encoding='utf-8') as f:
            json.dump(self.cfg, f, 
                      sort_keys=True, 
                      indent=4, 
                      ensure_ascii=False,
                      cls=DateTimeEncoder)


cfg = ConfigJson('project/chatbot_wenxin/config.json')