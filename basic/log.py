import os
import sys
import logging
from loguru import logger


def log_by_logging():
    """logging库管理日志"""

    # 创建日志器对象
    logger = logging.getLogger(__name__)

    # 设置logger可输出日志级别范围
    logger.setLevel(logging.DEBUG)

    # 添加控制台handler，用于输出日志到控制台
    console_handler = logging.StreamHandler()
    # 添加日志文件handler，用于输出日志到文件中
    file_handler = logging.FileHandler(filename='log.log', encoding='UTF-8')

    # 将handler添加到日志器中
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # 设置格式并赋予handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.info('这是一个info日志信息')
    logger.debug('这是一个debug日志信息')


def log_by_loguru():
    """loguru库管理日志"""

    # 删去import logger之后自动产生的handler
    # logger.remove(handler_id=None)

    # 将日志保存到本地
    logger.add("log_{time}.log", 
                level='INFO',
                rotation="100MB",             # 当日志文件达到500MB时就会重新生成一个文件
                encoding="utf-8",             # 编码方式
                enqueue=True,                 # 代表异步写入，多进程同时写入时会用到
                compression="zip",            # 压缩方式
                retention="100 days")         # 配置日志的最长保留时间

    logger.debug("中文loguru")
    logger.info("中文loguru")
    logger.warning("中文loguru")
    logger.error("中文loguru")


class Log():
    """loguru的封装
    Params
        level : 日志等级
        stdout: 是否输出日志到控制台
        logdir: 日志保存路径
        level : 日期等级
    """
    def __init__(self,
                 level='DEBUG',
                 stdout=True, 
                 logdir=False) -> None:
        self.logger = logger
        self.logger.remove()

        if stdout:
            # 日志输出到控制台
            self.logger.add(sys.stdout)

        if logdir:
            # 保存日志
            logname = os.path.join(logdir, '{time}.log')
            self.logger.add(logname, level=level,
                rotation="100MB", encoding="utf-8",
                enqueue=True, retention="100 days")

    def get_logger(self):
        return self.logger


if __name__ == "__main__":
    logger = Log().get_logger()

    logger.debug('这是一个debug')
    logger.info('这是一个info')
    logger.success('这是一个success')
    logger.warning('这是一个warning')