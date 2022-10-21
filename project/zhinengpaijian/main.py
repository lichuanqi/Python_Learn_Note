import re
import tqdm

import pandas as pd

class AILanTou:
    """
    代码重构
    """
    def __init__(self) -> None:


        print('开始程序初始化')
        # 时限数据保存为字典
        self.shixian_dict = self.get_shixian()
        print('-- 读取时限数据为字典')
        # 聚合点关键字保存为关键字
        self.gjz = self.get_keyword()
        print('-- 读取聚合点数据为关键字')

    
    def get_shixian(self):
        """
        读取时限数据表
        Args:
            shixian:
        Return:
            dict
        """
        shixian_path = 'D:\CPRI\项目6-智能派件\data_shixian.xlsx'
        shixian = pd.read_excel(shixian_path)

        shixian_dict = {}
        for index,row in shixian.iterrows():
            k = row[0] + '_' + row[1]
            v = row[2]
            shixian_dict[k] = v

        return shixian_dict

    
    def get_keyword(self):
        """
        读取关键字列表
        Args: 
            gjz_path: 育新关键字表.xls文件路径
        Return:
            gjz: 
        """
        gjz_path = 'D:\CPRI\项目6-智能派件\data_gjz.xls'
        gjz = pd.read_excel(gjz_path)
  
        # 计算关键字的字符长度
        gjz_len = list()
        for index,row in gjz.iterrows():
            gjz_len.append(len(''.join(row[1])))

        (g_min, g_max) = (min(gjz_len), max(gjz_len))
        print('最短关键词长度: {}\n最长关键词长度: {}'.format(g_min, g_max))

        gjz_dict_key = dict(zip(gjz['gjz'].values, gjz_len))

        return gjz_dict_key


    def str2words(self,s1):
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


    def qiongju(self,add_char:list, ns:int, nn:int):
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


    def zhuhang(self,toudi_path):
        """逐行计算
        Args
            toudi_path: 投递明细表路径
        """
        toudi = pd.read_csv(toudi_path)

        # 新建空列表保存数据
        leixings = []   # 邮件类型
        pincis = []     # 投递频次  
        juhedians = []   # 聚合点

        # 逐行循环
        print('开始逐行计算...')
        for index, row in toudi.iterrows():
 
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
            time_xiaduan = str(row['first_xiaduan'])
            if '/' in time_xiaduan:
                time_xiaduan_h = int(time_xiaduan.split(' ')[1].split(':')[0])
            else:
                time_xiaduan_h = 25

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
            print('i: %s, leixin: %s, pinci: %s, juhedian: %s'%(index, leixing, pinci, r))

        # 数据插入到表中
        self.df_new = toudi.copy()
        self.df_new.insert(4,column='leixings', value=leixings)
        self.df_new.insert(4,column='pincis', value=pincis)
        self.df_new.insert(4,column='juhedian', value=juhedians)
        
        print(self.df_new)
        
    def save_df_new(self, savepath):
        """
        数据保存到本地
        """
        self.df_new.to_csv(savepath, index=True, header=True)
        print('数据已保存至: %s'%(savepath))

        
if __name__=='__main__':

    toudi_path = 'D:\CPRI\项目6-智能派件\育新投递.csv'
    savepath = 'D:\CPRI\项目6-智能派件\育新投递_新.csv'

    run = AILanTou()
    run.zhuhang(toudi_path=toudi_path)
    run.save_df_new(savepath=savepath)