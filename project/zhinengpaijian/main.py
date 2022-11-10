import sys
import re
import os
import json

import math
import pandas as pd
import datetime

from log import log
from isPointinArea import isin_multipolygon


class Vividict(dict):
    """
    空的嵌套字典
    """
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


class AILanTou:
    """
    智能派件项目代码重构

    Args
        shixian_path : 时限数据读取路径
        ltb_path     : 揽投部基础信息
        gjz_path     : 聚合点关键字数据读取路径
        toudi_path   : 投递详细数据读取路径
        gps_path     : GPS数据路径
        savepath     : 数据保存路径

    Returns
        self.shixian_dict [dict]    : 时限数据
        self.ltb_area [[]]          : 揽投部电子围栏信息
        self.gjz [dcit]             : 聚合点关键字
        self.kd_selected [DataFrame]:
        self.bk_selected [DataFrame]:

    Output
        df_1day_add3.csv      : 新增邮件类型、投递频次、聚合点的数据
        jh_pincis.json        : 聚合点所有邮件的频次
        jh_pincis_gengxin.json: 聚合点频次更新情况
        self.jh_toudiren.json : 聚合点投递人员类型保存
        df_1day_update2.csv   : 更新聚合点的投递频次、投递人数据
    """
    def __init__(self, 
                 shixian_path,
                 ltb_path,
                 gjz_path, 
                 bk_path, 
                 kd_path, 
                 savepath
                 ) -> None:
        
        logger.info('开始程序初始化')
        
        # 时限数据
        logger.info(f'读取时限数据为字典: {shixian_path}')
        self.shixian_dict = self.get_shixian(shixian_path)

        # 揽投部基础信息
        logger.info(f'读取揽投部基础信息: {ltb_path}')
        self.get_ltb(ltb_path)
        
        # 聚合点数据
        logger.info(f'读取聚合点数据为关键字: {gjz_path}')
        self.gjz = self.get_keyword(gjz_path)
        
        # 快递和报刊的详细数据，并按条件筛选
        start = datetime.datetime.strptime('20220801 00:01', r'%Y%m%d %H:%M')
        end = datetime.datetime.strptime('20220801 23:59', r'%Y%m%d %H:%M')
        logger.info(f'筛选指定天的数据: [{start} - {end}]')
        self.kd_selected = self.read_and_select(kd_path, start, end)
        logger.info(f'快递: 共计 {len(self.kd_selected)} 条数据')
        self.bk_selected = self.read_and_select(bk_path, start, end)
        logger.info(f'报刊: 共计 {len(self.bk_selected)} 条数据')

        # 设置保存路径
        if savepath:
            if not os.path.exists(savepath):
                os.makedirs(savepath)
                logger.info(f'保存路径不存在，已新建文件夹: {savepath}')
            else:
                logger.info(f'保存路径存在: {savepath}')
            self.savepath = savepath
        else:
            self.savepath = None

            
    def get_shixian(self, shixian_path):
        """
        读取时限数据表
        Args:
            shixian:
        Return:
            dict
        """
        shixian = pd.read_excel(shixian_path)

        shixian_dict = {}
        for index,row in shixian.iterrows():
            k = row[0] + '_' + row[1]
            v = row[2]
            shixian_dict[k] = v

        return shixian_dict


    def get_ltb(self, ltb_path):
        """
        读取揽投部基础信息中的
        Args: 
            ltb_path: 揽投部基础信息
        Return:
            self.ltb_area: 揽投部电子围栏信息
        """
        ltb = json2dict(ltb_path)
        ltb_area = []
        for i in range(len(ltb['fence'])):
            ltb_area.append([float(ltb['fence'][i][0]), float(ltb['fence'][i][1])])

        self.ltb_area = ltb_area

    
    def get_keyword(self, gjz_path):
        """
        读取关键字列表
        Args: 
            gjz_path: 育新关键字表.xls文件路径
        Return:
            gjz: 
        """
        gjz = pd.read_excel(gjz_path)
  
        # 计算关键字的字符长度
        gjz_len = list()
        for index,row in gjz.iterrows():
            gjz_len.append(len(''.join(row[1])))

        g_min, g_max = min(gjz_len), max(gjz_len)
        logger.info(f'最短关键词长度: {g_min},最长关键词长度: {g_max}')

        gjz_dict_key = dict(zip(gjz['gjz'].values, gjz_len))

        return gjz_dict_key

    def read_and_select(self, data_path, start, end):
        """
        读取投递详细数据，并筛选指定天的数据
        """
        data = pd.read_excel(data_path, 'Sheet1')
        # 将时间转换为pd的格式
        data['下段时间'] = pd.to_datetime(data['下段时间'])

        # 按照要求选取数据
        bk_selected = data[((data['投递机构'] == 10009612) | (data['投递机构'] == 10009606)) &
                           (data['下段时间'] >= start) &
                           (data['下段时间'] <= end)]

        return bk_selected


    def zhu_hang_kd(self):
        """
        逐行计算快递数据的业务类型、邮件类型、投递频次、聚合点
        业务类型: 根据 [投递机构] 代码确定 10009606->普邮, 10009612->速递
        邮件类型: 使用表中的 [邮件种类3]
        投递频次: 根据 [下段时间]
        聚合点: 根据 [收件人地址]

        Args
            self.kd_selected [DataFrame]: 投递详细数据

        Return
            self.kd_selected_add3 [DataFrame]:

        Output
            kd_selected_add3.csv: 新增邮件类型、投递频次、聚合点的数据
        """
        kd_selected_add3 = self.kd_selected.copy()

        # 新增业务类型
        kd_selected_add3['yewu'] = kd_selected_add3.apply(lambda x: 
                                        '普邮' if  x['投递机构'] == 10009606 else '速递',axis=1)

        # 新建空列表保存数据
        pincis = []     # 投递频次  
        juhedians = []  # 聚合点

        logger.info('开始逐行计算投递频次、聚合点...')
        for index, row in kd_selected_add3.iterrows():

            # ========= 根据业务类型、邮件类型确定时限要求 =========
            leixing = row['yewu'] + '_' + row['邮件种类3']
            shixian = self.shixian_dict[leixing]

            # ========= 根据时限要求、下段时间确定频次 ========= 
            time_xiaduan_h = row['下段时间'].hour

            # 计算投递频次
            if time_xiaduan_h < 12:
                if shixian == '当频':
                    pinci = 1
                else:
                    pinci = 3
            elif time_xiaduan_h <= 24:
                pinci = 2
            else:
                pinci = 4
            pincis.append(pinci)

            # ========= 根据收件地址判断聚合点 =========
            addr = str(row['收件人地址'])
            # 根据长度过滤一些异常值
            if len(addr) > 9:
                addr = addr.replace('北京市', '')
                # 按字切分
                word_list = str2words(addr)
                # 根据切分结果进行穷举，并判断是否在关键词字典中
                qj = qiongju(word_list,2,8)
                r = None
                for q in qj:
                    qq = ''.join(q)
                    if qq in self.gjz.keys():
                        r = qq
            else:
                r = 'pass'

            juhedians.append(r)

            # ========= 以上几个结果输出一下 =========
            logger.debug(f'i: {index}, leixin: {leixing}, time_xiaduan_h: {time_xiaduan_h}, '
                f'pinci: {pinci}, juhedian: {r}')

        # 数据插入到表中
        kd_selected_add3.insert(4,column='pinci', value=pincis)
        kd_selected_add3.insert(4,column='juhedian', value=juhedians)

        self.kd_selected_add3 = kd_selected_add3

        if self.savepath:
            save_name = self.savepath + 'kd_selected_add3.csv'
            kd_selected_add3.to_csv(save_name, index=True, header=True)
            logger.info(f'SAVE 新增业务类型、投递频次、聚合点的数据保存至: {save_name}')


    def zhu_hang_bk(self):
        """
        逐行计算报刊数据的业务类型、邮件类型、投递频次、聚合点
        业务类型、邮件类型: 普邮_报刊
        投递频次: 根据 [下段时间]
        聚合点: 根据 [收件人地址]

        Args
            self.kd_selected [DataFrame]: 投递详细数据

        Return
            self.kd_selected_add3 [DataFrame]:

        Output
            kd_selected_add3.csv: 新增邮件类型、投递频次、聚合点的数据
        """
        bk_selected_add3 = self.bk_selected.copy()

        bk_selected_add3['yewu'] = '普邮'

        # 新建空列表保存数据
        pincis = []      # 投递频次  
        juhedians = []   # 聚合点

        logger.info('开始逐行计算投递频次、聚合点...')
        for index, row in bk_selected_add3.iterrows():

            # ========= 根据业务类型、邮件类型确定时限要求 =========
            leixing = '普邮_报刊'
            shixian = self.shixian_dict[leixing]

            # ========= 根据时限要求、下段时间确定频次 ========= 
            time_xiaduan_h = row['下段时间'].hour

            # 计算投递频次
            if time_xiaduan_h < 12:
                if shixian == '当频':
                    pinci = 1
                else:
                    pinci = 3
            elif time_xiaduan_h <= 24:
                pinci = 2
            else:
                pinci = 4
            pincis.append(pinci)

            # ========= 根据收件地址判断聚合点 =========
            addr = str(row['报刊投递地址'])
            # 根据长度过滤一些异常值
            addr = addr.replace('北京市', '')
            # 按字切分
            word_list = str2words(addr)
            # 根据切分结果进行穷举，并判断是否在关键词字典中
            qj = qiongju(word_list,2,8)
            r = None
            for q in qj:
                qq = ''.join(q)
                if qq in self.gjz.keys():
                    r = qq

            juhedians.append(r)

            # ========= 以上几个结果输出一下 =========
            logger.debug(f'i: {index}, leixin: {leixing}, time_xiaduan_h: {time_xiaduan_h}, '
                f'pinci: {pinci}, juhedian: {r}')

        # 数据插入到表中
        bk_selected_add3.insert(4,column='pinci', value=pincis)
        bk_selected_add3.insert(4,column='juhedian', value=juhedians)

        self.bk_selected_add3 = bk_selected_add3

        if self.savepath:
            save_name = self.savepath + 'bk_selected_add3.csv'
            bk_selected_add3.to_csv(save_name, index=True, header=True)
            logger.info(f'SAVE 新增业务类型、投递频次、聚合点的数据保存至: {save_name}')


    def zhu_juhedian(self):
        """
        统计每个聚合点的邮件数量、频次，确定频次更新情况和投递人

        Args
            self.df_1day_add3 [DateFrame]: 
        
        Return
            self.jh_toudiren [dict]: 聚合点投递人员类型
            self.df_1day_update2 [DateFrame]: 
            jhs [dict]: 
                        jhs = {'聚合点1': {'速递': {'pincis': [],
                                                   'leixings': [],
                                                   'num': 0},
                                          '普服': {'pincis': [],
                                                  'leixing': [],
                                                  'num': 0},
                                          '频次更新': '',
                                          '投递人': ''
                                        }
                            }

        Output
            jhd.json              : 聚合点所有邮件的频次
            df_1day_update2.csv   : 更新聚合点的投递频次、投递人数据
        """
        logger.info('统计每个聚合点的邮件数量、频次，确定频次更新情况和投递人...')

        # 逐行循环记录每个聚合点的邮件类型和频次
        jhs = {}
        logger.info('逐行循环记录每个聚合点的邮件类型和频次: 速递')
        for index, row in self.kd_selected_add3.iterrows():
            juhedian = row['juhedian']
            leixing = row['yewu']
            pinci = row['pinci']
            
            # 聚合点名称第一次出现时格式化数据
            if juhedian not in jhs.keys():
                jhs[juhedian] = {'速递': {'pincis': [],
                                         'yewus': [],
                                         'num': 0},
                                 '普邮': {'pincis': [],
                                         'yewus': [],
                                         'num': 0},
                                 '频次更新': '',
                                 '投递人': '',
                                 '总数量': 0
                                }

            # 更新数据
            jhs[juhedian][leixing]['pincis'].append(pinci)
            jhs[juhedian][leixing]['yewus'].append(leixing)
            jhs[juhedian][leixing]['num'] += 1
            jhs[juhedian]['总数量'] += 1

        logger.info('逐行循环记录每个聚合点的邮件类型和频次: 报刊')
        for index, row in self.bk_selected_add3.iterrows():
            juhedian = row['juhedian']
            leixing = row['yewu']
            pinci = row['pinci']
            
            # 聚合点名称第一次出现时格式化数据
            if juhedian not in jhs.keys():
                jhs[juhedian] = {'速递': {'pincis': [],
                                         'yewus': [],
                                         'num': 0},
                                 '普邮': {'pincis': [],
                                         'yewus': [],
                                         'num': 0},
                                 '频次更新': '',
                                 '投递人': '',
                                 '总数量': 0
                                }
            # 更新数据
            jhs[juhedian][leixing]['pincis'].append(pinci)
            jhs[juhedian][leixing]['yewus'].append(leixing)
            jhs[juhedian][leixing]['num'] += 1
            jhs[juhedian]['总数量'] += 1

        # 逐聚合点确定频次更新情况和投递人
        logger.info('逐聚合点确定频次更新情况和投递人')
        for key, value in jhs.items():
            
            # 更新频次
            values = value['速递']['pincis'] + value['普邮']['pincis']
            ONE, TWO, THREE = 1 in values, 2 in values, 3 in values
            
            if not ONE and TWO and THREE:     # 3 -> 1
                jhs[key]['频次更新'] = '3->2'
            elif  THREE:
                jhs[key]['频次更新'] = '3->1'
            else:
                jhs[key]['频次更新'] = '不变'

            # 确定投递人
            if value['普邮']['num'] >= value['速递']['num']:
                value['投递人'] = '普邮'             
            else:
                value['投递人'] = '速递'

        self.jhs = jhs
        if self.savepath:
            savename_1 = self.savepath + 'jhs.json'
            save_dict2json(jhs, savename_1)
            logger.info(f'聚合点所有邮件频次、类型、数量保存至: {savename_1}')

    
    def update_pinci_toudiren(self):
        """
        将聚合点的频次更新情况和投递人更新到表中
        """

        logger.info('将计算得到的每个聚合点的投递频次和投递人员更新到表中: 速递')
        kd_selected_update2 = self.kd_selected_add3.copy()
        kd_selected_update2['pinci_update'] = ' '
        kd_selected_update2['toudiren'] = ' '

        for index, row in kd_selected_update2.iterrows():
            
            # 更新频次信息
            juhedian = row['juhedian']
            if row['pinci'] == 3:
                if self.jhs[juhedian]['频次更新'] == '3->1':
                    kd_selected_update2.loc[index,'pinci_update'] = 1
                elif self.jhs[juhedian]['频次更新'] == '3->2':
                    kd_selected_update2.loc[index,'pinci_update'] = 2
            else:
                kd_selected_update2.loc[index,'pinci_update'] = row['pinci']
            
            # 更新投递人信息
            kd_selected_update2.loc[index,'toudiren'] = self.jhs[juhedian]['投递人']

        self.kd_selected_update2 = kd_selected_update2
        if self.savepath:
            save_name_11 = self.savepath + 'kd_selected_update2.csv'
            kd_selected_update2.to_csv(save_name_11, index=True, header=True)
            logger.info(f'更新聚合点的投递频次、投递人数据保存至: {save_name_11}')

        logger.info('将计算得到的每个聚合点的投递频次和投递人员更新到表中: 报刊')
        bk_selected_update2 = self.bk_selected_add3.copy()
        bk_selected_update2['pinci_update'] = ' '
        bk_selected_update2['toudiren'] = ' '

        for index, row in bk_selected_update2.iterrows():
            
            # 更新频次信息
            juhedian = row['juhedian']
            if row['pinci'] == 3:
                if self.jhs[juhedian]['频次更新'] == '3->1':
                    bk_selected_update2.loc[index,'pinci_update'] = 1
                elif self.jhs[juhedian]['频次更新'] == '3->2':
                    bk_selected_update2.loc[index,'pinci_update'] = 2
            else:
                bk_selected_update2.loc[index,'pinci_update'] = row['pinci']
            
            # 更新投递人信息
            bk_selected_update2.loc[index,'toudiren'] = self.jhs[juhedian]['投递人']

        self.bk_selected_update2 = bk_selected_update2
        if self.savepath:
            save_name_11 = self.savepath + 'bk_selected_update2.csv'
            bk_selected_update2.to_csv(save_name_11, index=True, header=True)
            logger.info(f'更新聚合点的投递频次、投递人数据保存至: {save_name_11}')

            
    def get_orders(self):
        """
        根据明细表提取每个普邮和速递最终的投递点经纬度数据

        Args
            self.kd_selected_update2 [DateFrame]:
            self.bk_selected_update2 [DateFrame]:

        Return
            orders: 

        Output
            orders.json: 

        """
        logger.info('根据明细表和确定的投递人提取普邮和速递最终的投递点经纬度数据')

        # A 聚合点数据结构
        orders_AA = {'1频': {'速递': [],
                             '普邮': []},
                     '2频': {'速递': [],
                             '普邮': []}
                    }
        # B 聚合点数据结构
        orders_BB = {'1频': {'外部': [],
                             '内部': {}},
                     '2频': {'外部': [],
                             '内部': {}}
                    }

        order_1_sudi = []
        order_2_sudi = []
        order_1_puyou = []
        order_2_puyou = []

        order_jhd_1_wai = []
        order_jhd_1_nei = {}
        order_jhd_2_wai = []
        order_jhd_2_nei = {}
        
        wai_num = 0 

        # 速递
        for index, row in self.kd_selected_update2.iterrows():

            order_id = 'kd_' + str(index)
            juhedian = row['juhedian']
            pinci = row['pinci_update']
            toudiren = row['toudiren']
            lng = row['lng']
            lat = row['lat']
            
            # 派件点GPS坐标转为百度坐标系
            lng_new, lat_new = gps_GCJ02toBD09(lng, lat)

            # 根据经纬度坐标判断是否在电子围栏内
            point = (lng_new, lat_new)
            if not isin_multipolygon(point, self.ltb_area, contain_boundary=True):
                logger.debug(f'速递 {index} 不在电子围栏内跳过')
                wai_num += 1
                continue
            
            order = {"order_id": order_id,
                    "longitude": lng_new,
                    "latitude": lat_new,
                    "begin_time": "12:00",
                    "leave_time": "16:00",
                    "number": 1,
                    'transaction_duration': 120}

            if pinci == 1:
                # A - 每个聚合点的所有派件点
                if toudiren == '速递':
                    order_1_sudi.append(order)
                else:
                    order_1_puyou.append(order)

                # B - 外部只存放聚合点出现的第一个点
                if juhedian not in order_jhd_1_nei.keys():
                    order_jhd_1_wai.append(order)
                    order_jhd_1_nei[juhedian] = []
                # B - 内部存放聚合点的所有点
                order_jhd_1_nei[juhedian].append(order)

            elif pinci == 2:
                # A - 每个聚合点的所有派件点
                if toudiren == '普邮':
                    order_2_sudi.append(order)
                else:
                    order_2_puyou.append(order)

                # B - 外部只存放聚合点出现的第一个点
                if juhedian not in order_jhd_2_nei.keys():
                    order_jhd_2_wai.append(order)
                    order_jhd_2_nei[juhedian] = []
                # B - 内部存放聚合点的所有点
                order_jhd_2_nei[juhedian].append(order)
            else:
                pass

        # 报刊
        for index, row in self.bk_selected_update2.iterrows():

            order_id = 'bk_' + str(index)
            juhedian = row['juhedian']
            pinci = row['pinci_update']
            toudiren = row['toudiren']
            lng = row['lng']
            lat = row['lat']

            # 派件点GPS坐标转为百度坐标系
            lng_new, lat_new = gps_GCJ02toBD09(lng, lat)

            # 根据经纬度坐标判断是否在电子围栏内
            point = (lng_new, lat_new)
            if not isin_multipolygon(point, self.ltb_area, contain_boundary=True):
                logger.debug(f'报刊 {index} 不在电子围栏内跳过')
                wai_num += 1
                continue
            
            order = {"order_id": order_id,
                    "longitude": lng_new,
                    "latitude": lat_new,
                    "begin_time": "12:00",
                    "leave_time": "16:00",
                    "number": 1,
                    'transaction_duration': 120}

            if pinci == 1:
                # A - 聚合点的所有点按照类型、频次存放
                if toudiren == '速递':
                    order_1_sudi.append(order)
                else:
                    order_1_puyou.append(order)

                # B - 外部只存放聚合点出现的第一个点
                if juhedian not in order_jhd_1_nei.keys():
                    order_jhd_1_wai.append(order)
                    order_jhd_1_nei[juhedian] = []
                # B - 内部存放聚合点的所有点
                order_jhd_1_nei[juhedian].append(order)

            elif pinci == 2:
                # A - 每个聚合点的所有派件点
                if toudiren == '普邮':
                    order_2_sudi.append(order)
                else:
                    order_2_puyou.append(order)

                # B - 外部只存放聚合点出现的第一个点
                if juhedian not in order_jhd_2_nei.keys():
                    order_jhd_2_wai.append(order)
                    order_jhd_2_nei[juhedian] = []
                # B - 内部存放聚合点的所有点
                order_jhd_2_nei[juhedian].append(order)
            else:
                pass

        logger.info(f'共跳过 {wai_num} 个围栏外的派件点')

        # 保存数据 - A
        logger.info(f'速递_1频: {len(order_1_sudi)} 个, 速递_2频: {len(order_2_sudi)} 个, '
            f'普邮_1频: {len(order_1_puyou)} 个, 普邮_2频: {len(order_2_puyou)} 个')
        orders ={'速递_1频': order_1_sudi, '普邮_1频': order_1_puyou,
            '速递_2频': order_2_sudi, '普邮_2频': order_2_puyou}
        savename_1 = self.savepath + 'orders_A.json'
        save_dict2json(orders, savename_1)
        logger.info(f'A方案派件点数据保存至: {savename_1}')

        i = 1
        for key,value in order_jhd_1_nei.items(): 
            logger.info(f'聚合点{i}: {key}, 派件点数量: {len(value)}')
            i += 1

        # 保存数据 - B - 每个聚合点一个点坐标
        logger.info(f'1频共 {len(order_jhd_1_wai) } 个派件聚合点, 2频: {len(order_jhd_2_wai)}')
        orders_B = {'1频': {'整体': order_jhd_1_wai,
                            '每个聚合点': order_jhd_1_nei},
                    '2频': {'整体': order_jhd_2_wai,
                            '每个聚合点': order_jhd_2_nei}
                    }
        savename_2 = self.savepath + 'orders_B.json'
        save_dict2json(orders_B, savename_2)
        logger.info(f'B方案派件点数据保存至: {savename_2}')


def str2words(s1) -> list:
    """
    把句子按字分开，中文按字分，英文按单词，数字按空格
    北京市北京市昌平区回龙观街道东村家园A10号楼7单元Tuesday
    -> ['北', '京', '市', '北', '京', '市', '昌', '平', '区', 
        '回', '龙', '观', '街', '道', '东', '村', '家', '园', 
        'a10', '号', '楼', '7', '单', '元', 'tuesday']
    """
    # regEx = re.compile('[\\W]*')    # 我们可以使用正则表达式来切分句子，切分的规则是除单词，数字外的任意字符串
    regEx = re.compile('\W+')
    res = re.compile(r"([\u4e00-\u9fa5])")    #  [\u4e00-\u9fa5]中文范围

    p1 = regEx.split(s1.lower())
    str1_list = []
    for str in p1:
        if res.split(str) == None:
            str1_list.append(str)
        else:
            ret = res.split(str)
            for ch in ret:
                str1_list.append(ch)

    list_word1 = [w for w in str1_list if len(w.strip()) > 0]  # 去掉为空的字符

    return  list_word1


def qiongju(add_char:list, ns:int, nn:int) -> list:
    """
    根据切分结果排列组合结果
    ['回', '龙', '观', '街', '道', '东', '村', '家', '园', '甲', '10', '号', '楼', '7', '单', '元', 'tuesday']
    ->  回龙观: False
        龙观街: False
        单元tuesday: False
        回龙观街: False
        7单元tuesday: False
        楼7单元tuesday: False
        ...
    """
    results = list()
    for i in range(ns, nn):
        for j in range(0,len(add_char)-i+1):
            res = add_char[j:j+i]
            results.append(res)
    return results


def save_dict2json(dicts, savename):
    """
    字典保存为json文件
    Args
        dicts [dict]:
        savename [str]:
    Return
        savename.json:
    """
    with open(savename, "w") as f:
        f.write(json.dumps(dicts, ensure_ascii=False, indent=4, separators=(',', ':')))


def json2dict(json_path):

    with open(json_path, 'r') as f:
        orders = json.load(f)

    return orders


def gps_GCJ02toBD09(lng, lat):
    """
    腾讯gps坐标转换为百度
    Arg
        lng, lat: GCJ-02 火星坐标系

    Return
        lng, lat: GCJ-02 BD09坐标系
    """
    lng_pi = 3.14159265358979324 * 3000.0 / 180.0
 
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * lng_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * lng_pi)
    lat_new = z * math.sin(theta) + 0.006     #0.006     #0.01205
    lng_new = z * math.cos(theta) + 0.0062    #0.0065    #0.00370

    # 保留6位小数点
    lng_new, lat_new = float('%.6f'%lng_new), float('%.6f'%lat_new)

    return lng_new, lat_new


if __name__=='__main__':

    # 基础数据
    shixian_path = 'D:\CPRI\项目6-智能派件\data_shixian.xlsx'
    ltb_path = 'D:\CPRI\项目6-智能派件\data_lantoubu.json'
    gjz_path = 'D:\CPRI\项目6-智能派件\data_gjz.xls'

    # 报刊数据
    bk_path = "D:\CPRI\项目6-智能派件\data-1101\data_bk_20220801.xlsx"
    # 快递数据
    kd_path = "D:\CPRI\项目6-智能派件\data-1101\data_kd_20220801.xlsx"

    # 结果保存路径
    savepath = 'D:/CPRI/项目6-智能派件/output_1110_wt-60/'

    logger = log(savepath).get_logger()

    run = AILanTou(shixian_path = shixian_path,
                   ltb_path = ltb_path,
                   gjz_path = gjz_path,
                   bk_path = bk_path,
                   kd_path = kd_path,
                   savepath = savepath)
    run.zhu_hang_kd()
    run.zhu_hang_bk()
    
    run.zhu_juhedian()

    run.update_pinci_toudiren()
    run.get_orders()