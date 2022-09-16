# 合并 收寄、投递 两个表的数据

import pandas as pd
import logging


# 创建日志器对象
logger = logging.getLogger(__name__)
# 设置logger可输出日志级别范围
logger.setLevel(logging.DEBUG)
# 添加控制台handler，用于输出日志到控制台
console_handler = logging.StreamHandler()
# 将handler添加到日志器中
logger.addHandler(console_handler)
# 设置格式并赋予handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

sj_path = "D:/CPRI/项目-3-两集中仿真/数据-揽投机构/SELECT_t___FROM_cpdl_tmp_sj_jigou_t.csv"
td_path = "D:/CPRI/项目-3-两集中仿真/数据-揽投机构/SELECT_t___FROM_cpdl_tmp_td_jigou_t.csv"

delivery_path_1 = "D:/CPRI/项目-3-两集中仿真/基础表-delivery_org-20220916_1.csv"
delivery_path_2 = "D:/CPRI/项目-3-两集中仿真/基础表-delivery_org-20220916_2.csv"

sj = pd.read_csv(sj_path,header=None)
td = pd.read_csv(td_path,header=None)

de_list = []
# de_list: [[de_id, de_name, de_fun]]
#   de_id: 揽投机构id
#   de_name：揽投机构名称
#   de_fun：揽投机构功能代码 1：收寄 2:投递 3：收寄+投递

# 遍历收寄表，判断揽投机构是否在投机表中
# 在投机表   ->  揽投机构功能: 收寄+投递 
# 不在投机表 ->  揽投机构功能: 收寄
logger.info('遍历收寄表')
for index,row in sj.iterrows():

    de_id, de_name = row[0], row[1]

    if de_id in td.loc[:,0].to_list():
        logger.info('{} is in td, fun: sj,td '.format(de_id))
        de_fun = 3
    else:
        logger.info('{} is not in td, fun: sj'.format(de_id))
        de_fun = 1

    de_list.append([de_id, de_name, de_fun])

de_pf = pd.DataFrame(data=de_list,
            columns=['de_id', 'de_name', 'de_fun'])
print(de_pf)
de_pf.to_csv(delivery_path_1)

# 遍历投递表
logger.info('遍历投递表')
for index,row in td.iterrows():
    de_id, de_name = row[0], row[1]

    if de_id in sj.loc[:,0].to_list():
        logger.info('{} is in sj, fun: sj,td, pass '.format(de_id))
    else:
        logger.info('{} is not in sj, fun: td'.format(de_id))
        de_fun = 2
        de_list.append([de_id, de_name, de_fun])

de_pf = pd.DataFrame(data=de_list,
            columns=['de_id', 'de_name', 'de_fun'])
print(de_pf)
de_pf.to_csv(delivery_path_2)