import re
import os
import json

import pandas as pd
import datetime


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


class AILanTou:
    """
    智能派件项目代码重构

    Args
        shixian_path : 时限数据读取路径
        gjz_path     : 聚合点关键字数据读取路径
        toudi_path   : 投递详细数据读取路径
        gps_path     : GPS数据路径
        savepath     : 数据保存路径

    Output
        df_1day_add3.csv      : 新增邮件类型、投递频次、聚合点的数据
        jh_pincis.json        : 聚合点所有邮件的频次
        jh_pincis_gengxin.json: 聚合点频次更新情况
        self.jh_toudiren.json : 聚合点投递人员类型保存
        df_1day_update2.csv   : 更新聚合点的投递频次、投递人数据
    """
    def __init__(self, shixian_path, gjz_path, toudi_path, gps_path, savepath) -> None:
        
        print('开始程序初始化')
        # 时限数据保存为字典
        self.shixian_dict = self.get_shixian(shixian_path)
        print(f'-- 读取时限数据为字典: {shixian_path}')
        # 聚合点关键字保存为关键字
        self.gjz = self.get_keyword(gjz_path)
        print(f'-- 读取聚合点数据为关键字: {gjz_path}')
        # 读取投递详细数据，并筛选指定天的数据
        s_data = datetime.datetime.strptime('20220601 00:01', r'%Y%m%d %H:%M')
        e_data = datetime.datetime.strptime('20220601 23:59', r'%Y%m%d %H:%M')
        self.toudi_1day = self.read_and_select(toudi_path, s_data, e_data)
        print(f'-- 筛选指定天的数据: [{s_data} - {e_data}]')
        print(f'-- 共计 {len(self.toudi_1day)} 条数据')
        # 读取GPS数据
        self.gpss = pd.read_csv(gps_path, header=0, index_col=0)
        print(f'读取GPS数据到 DataFrame: {gps_path}')
    
        # 设置保存路径
        if savepath:
            if not os.path.exists(savepath):
                os.makedirs(savepath)
                print(f'-- 保存路径不存在，已新建文件夹: {savepath}')
            else:
                print(f'-- 保存路径存在: {savepath}')
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

        (g_min, g_max) = (min(gjz_len), max(gjz_len))
        print('---- 最短关键词长度: {}\n---- 最长关键词长度: {}'.format(g_min, g_max))

        gjz_dict_key = dict(zip(gjz['gjz'].values, gjz_len))

        return gjz_dict_key
    

    def read_and_select(self, toudi_path, s_data, e_data):
        """
        读取投递详细数据，并筛选指定天的数据
        """
        toudi = pd.read_csv(toudi_path)
        # 将时间转换为pd的格式
        toudi['first_xiaduan'] = pd.to_datetime(toudi['first_xiaduan'])
        # 按照时间排序
        toudi_date = toudi.sort_values(by='first_xiaduan')

        # 按照范围选取数据
        toudi_date_1 = toudi_date[(toudi_date['first_xiaduan'] >= s_data) & \
                                  (toudi_date['first_xiaduan'] <= e_data)]
        # print(toudi_date_1)
        # toudi_date_1.to_csv('D:\CPRI\项目6-智能派件\育新投递_data_20220602.csv')

        return toudi_date_1

    
    def str2words(self,s1) -> list:
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

    def qiongju(self,add_char:list, ns:int, nn:int) -> list:
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

    def zhu_hang(self):
        """
        逐行计算邮件类型、投递频次、聚合点

        Args
            self.toudi_1day [DataFrame]: 投递详细数据

        Return
            self.df_1day_add3 [DataFrame]:

        Output
            df_1day_add3.csv: 新增邮件类型、投递频次、聚合点的数据
        """
        # 新建空列表保存数据
        leixings = []   # 邮件类型
        pincis = []     # 投递频次  
        juhedians = []  # 聚合点

        # 逐行循环
        print('开始逐行计算邮件类型、投递频次、聚合点...')
        for index, row in self.toudi_1day.iterrows():
 
            # ========= 根据运单号判断邮件类型 =========
            danhao = str(row['waybill_no'])
            leixing1 = '速递' if danhao[0:2] == '1.' else '普邮'
            leixing2 = str(row['business_prodduct_name'])
            try:
                shixian = self.shixian_dict[leixing1 + '_' + leixing2]
                leixing = leixing1
            except KeyError:
                shixian = self.shixian_dict['速递_' + leixing2]
                leixing = '速递'
            leixings.append(leixing)

            # ========= 根据邮件类型、时限要求、下段时间确定频次 ========= 
            time_xiaduan_h = row['first_xiaduan'].hour

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
            addr = str(row['receiver_addr'])
            # 根据长度过滤一些异常值
            if len(addr) > 9:
                addr = addr.replace('北京市北京市昌平区', '')
                # 按字切分
                word_list = self.str2words(addr)
                # 根据切分结果进行穷举，并判断是否在关键词字典中
                qj = self.qiongju(word_list,2,8)
                r = None
                for q in qj:
                    qq = ''.join(q)
                    if qq in self.gjz.keys():
                        r = qq
            else:
                r = 'pass'

            juhedians.append(r)

            # ========= 以上几个结果输出一下 =========
            print(f'i: {index}, leixin: {leixing}, time_xiaduan_h: {time_xiaduan_h}, \
                pinci: {pinci}, juhedian: {r}')

        # 数据插入到表中
        self.df_1day_add3 = self.toudi_1day.copy()
        self.df_1day_add3.insert(4,column='leixings', value=leixings)
        self.df_1day_add3.insert(4,column='pincis', value=pincis)
        self.df_1day_add3.insert(4,column='juhedian', value=juhedians)

        if self.savepath:
            save_name = self.savepath + 'df_1day_add3.csv'
            self.df_1day_add3.to_csv(save_name, index=True, header=True)
            print(f'-- SAVE 新增邮件类型、投递频次、聚合点的数据保存至: {save_name}')
        
    def zhu_juhedian(self):
        """
        逐聚合点更新邮件投递频次和投递人

        Args
            self.df_1day_add3 [DateFrame]: 
        
        Return
            self.jh_toudiren [dict]: 聚合点投递人员类型
            self.df_1day_update2 [DateFrame]: 

        Output
            jh_pincis.json        : 聚合点所有邮件的频次
            jh_pincis_gengxin.json: 聚合点频次更新情况
            jh_toudiren.json      : 聚合点投递人员类型保存
            df_1day_update2.csv   : 更新聚合点的投递频次、投递人数据
        """
        print('开始统计每个聚合点的邮件类型和频次...')

        # 读取数据按照聚合点顺序排序
        df_1day_update2 = self.df_1day_add3.sort_values(by='juhedian')

        # 逐行循环记录每个聚合点的邮件类型和频次
        print('-- 逐行循环记录每个聚合点的邮件类型和频次')
        jh_pincis = {}
        jh_leixing = {}
        for index, row in df_1day_update2.iterrows():
            
            juhedian = row['juhedian']
            leixing = row['leixings']
            pinci = row['pincis']
            
            if juhedian in jh_pincis.keys():
                jh_pincis[juhedian].append(pinci)
                jh_leixing[juhedian].append(leixing)
            else:
                jh_pincis[juhedian] = list()
                jh_leixing[juhedian] = list()
        
        # 逐聚合点判断投递频次是否需要更新
        print('-- 逐聚合点判断投递频次是否需要更新')
        jh_pinci_update = {}
        for key, values in jh_pincis.items():

            ONE, TWO, THREE = 1 in values, 2 in values, 3 in values
            
            if not ONE and TWO and THREE:     # 3 -> 1
                jh_pinci_update[key] = '3->2'
            elif  THREE:
                jh_pinci_update[key] = '3->1'
            else:
                jh_pinci_update[key] = '不变'

        # 逐聚合点判断由谁投递
        print('-- 逐聚合点判断由谁投递')
        self.jh_toudiren = {}
        for key, values in jh_leixing.items():
            # 统计'普邮'和'速递'数量
            jh_lx = {'普邮': 0, '速递': 0, '投递人':''}
            for v in values:
                if v in jh_lx.keys():
                    jh_lx[v] += 1

            if jh_lx['普邮'] > jh_lx['速递']:
                jh_lx['投递人'] = '普邮'                
            else:
                jh_lx['投递人'] = '速递'

            self.jh_toudiren[key] = jh_lx
        
        if self.savepath:
            # 聚合点所有邮件的频次
            savename_1 = self.savepath + 'jh_pincis.json'
            save_dict2json(jh_pincis, savename_1)
            print(f'-- SAVE 聚合点所有邮件的频次保存至: {savename_1}')
            # 聚合点的更新情况
            savename_2 = self.savepath + 'jh_pincis_gengxin.json'
            save_dict2json(jh_pinci_update, savename_2)
            print(f'-- SAVE 聚合点频次更新情况保存至: {savename_2}')
            # 聚合点投递人员类型
            savename_3 = self.savepath + 'jh_toudiren.json'
            save_dict2json(self.jh_toudiren, savename_3)
            print(f'-- SAVE 聚合点投递人员类型保存至: {savename_3}')

        # 将计算得到的每个聚合点的投递频次和投递人员更新到表中
        df_1day_update2['pinci_update'] = ' '
        df_1day_update2['toudiren'] = ''

        for index, row in df_1day_update2.iterrows():
            jhd = row['juhedian']
            # 更新频次信息
            if row['pincis'] == 3:
                if jh_pinci_update[jhd] == '3->1':
                    df_1day_update2.loc[index,'pinci_update'] = 1
                elif jh_pinci_update[jhd] == '3->2':
                    df_1day_update2.loc[index,'pinci_update'] = 2
            else:
                df_1day_update2.loc[index,'pinci_update'] = row['pincis']
            # 更新投递人信息
            df_1day_update2.loc[index,'toudiren'] = self.jh_toudiren[jhd]['投递人']

        self.df_1day_update2 = df_1day_update2
        if self.savepath:
            save_name_11 = self.savepath + 'df_1day_update2.csv'
            df_1day_update2.to_csv(save_name_11, index=True, header=True)
            print(f'-- SAVE 更新聚合点的投递频次、投递人数据保存至: {save_name_11}')

            
    def get_orders(self):
        """
        根据明细表和确定的投递人提取普邮和速递最终的投递点经纬度数据

        Args
            self.df_1day_update2 [DateFrame]:
            self.gpss [DateFrame]:

        Return
            orders: 

        Output
            orders.json: 

        """
        print('根据明细表和确定的投递人提取普邮和速递最终的投递点经纬度数据')

        order_1_sudi = []
        order_2_sudi = []
        order_1_puyou = []
        order_2_puyou = []

        for index, row in self.df_1day_update2.iterrows():
            pinci = row['pinci_update']
            toudiren = row['toudiren']

            order = {"order_id": index,
                "longitude": self.gpss.loc[index, 'lng'],
                "latitude": self.gpss.loc[index, 'lat'],
                "begin_time": "12:00",
                "leave_time": "16:00",
                "number": 1,
                'transaction_duration': 120}
            
            # TODO: 增加经纬度判别
            if pinci == 1:
                if toudiren == '速递':
                    order_1_sudi.append(order)
                else:
                    order_1_puyou.append(order)
            elif pinci == 2:
                if toudiren == '普邮':
                    order_2_sudi.append(order)
                else:
                    order_2_puyou.append(order)
            else:
                pass
        
        # 保存数据
        orders ={'速递_1频': order_1_sudi, '普邮_1频': order_1_puyou, \
                 '速递_2频': order_2_sudi, '普邮_2频': order_2_puyou} 
        savename_1 = self.savepath + 'orders.json'
        save_dict2json(orders, savename_1)
        print(f'-- SAVE 投递点经纬度数据保存至: {savename_1}')


if __name__=='__main__':

    shixian_path = 'D:\CPRI\项目6-智能派件\data_shixian.xlsx'
    gjz_path = 'D:\CPRI\项目6-智能派件\data_gjz.xls'
    toudi_path = 'D:/CPRI/项目6-智能派件/育新投递.csv'
    gps_path = 'D:/CPRI/项目6-智能派件/data_gps_1027.csv'
    savepath = 'D:/CPRI/项目6-智能派件/output-1028/'

    # run = AILanTou(shixian_path = shixian_path,
                #    gjz_path = gjz_path,
                #    toudi_path = toudi_path,
                #    gps_path=gps_path,
                #    savepath = savepath)
    # run.zhu_hang()
    # run.zhu_juhedian()
    # run.get_orders()