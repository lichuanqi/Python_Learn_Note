from loguru import logger


# 删去import logger之后自动产生的handler
# logger.remove(handler_id=None)

# 将日志保存到本地
logger.add("log_{time}.log", 
            level='INFO',
            rotation="100MB",             # 当日志文件达到500MB时就会重新生成一个文件
            encoding="utf-8",             # 编码方式
            enqueue=True,                 # 代表异步写入，多进程同时写入时会用到
            compression="zip",            # 压缩方式
            retention="10 days")          # 配置日志的最长保留时间

logger.debug("中文loguru")
logger.info("中文loguru")
logger.warning("中文loguru")
logger.error("中文loguru")
