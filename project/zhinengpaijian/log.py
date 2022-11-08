import sys
from loguru import logger


class log():
    def __init__(self) -> None:
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 添加控制台输出的格式,sys.stdout为输出到屏幕
        self.logger.add(sys.stdout)

    def get_logger(self):
        return self.logger