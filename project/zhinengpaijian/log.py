import sys
from loguru import logger


class log():
    def __init__(self, savepath=False) -> None:
        self.logger = logger
        # 清空所有设置
        self.logger.remove()

        if savepath:
            # 如果存在保存路径就生成日志文件
            logname =  savepath + 'log_{time}.log'
            self.logger.add(logname)
        
        # 不存在保存路径日志输出到控制台
        self.logger.add(sys.stdout)

    def get_logger(self):
        return self.logger