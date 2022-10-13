import sys
import time
import pandas as pd

import re


def get_keyword(gjz_path) -> dict:
    """
    读取关键字列表
    Args: 
        gjz_path: 育新关键字表.xls文件路径
    Return:
        gjz: 
    """
    gjz_path = 'D:\CPRI\项目6-智能派件\育新关键字表.xls'
    gjz = pd.read_excel(gjz_path)
    print('读取关键字列表到 gjz')
    # print(gjz)

    # 计算关键字的字符长度
    gjz_len = list()
    for index,row in gjz.iterrows():
        gjz_len.append(len(''.join(row[1])))
    # 将关键字的字符长度插入到dataframe中
    # gjz.insert(2,column='gjz_len', value=gjz_len)

    (g_min, g_max) = (min(gjz_len), max(gjz_len))
    print('最短关键词长度: {}\n最长关键词长度: {}\n'.format(g_min, g_max))

    gjz_dict_key = dict(zip(gjz['gjz'].values, gjz_len))

    # de_id_df = df['address'].values
    # de_id_list = df['address'].values.tolist()
    # de_id_dict_value = df['address'].to_dict()
    # gjz_dict_key = dict(zip(gjz['gjz'].values, gjz['gjz_len'].values))
    # de_id_set = set(df['address'].values)

    return gjz_dict_key


def get_word_list(s1):
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
        观街道: False
        街道东: False
        道东村: False
        东村家: False
        村家园: False
        家园甲: False
        园甲10: False
        甲10号: False
        10号楼: False
        号楼7: False
        楼7单: False
        7单元: False
        单元tuesday: False
        回龙观街: False
        龙观街道: False
        观街道东: False
        街道东村: False
        道东村家: False
        东村家园: True
        村家园甲: False
        家园甲10: False
        园甲10号: False
        甲10号楼: False
        10号楼7: False
        号楼7单: False
        楼7单元: False
        7单元tuesday: False
        回龙观街道: False
        龙观街道东: False
        观街道东村: False
        街道东村家: False
        道东村家园: False
        东村家园甲: False
        村家园甲10: False
        家园甲10号: False
        园甲10号楼: False
        甲10号楼7: False
        10号楼7单: False
        号楼7单元: False
        楼7单元tuesday: False
    """
    results = list()
    for i in range(ns, nn):
        for j in range(0,len(add_char)-i+1):
            res = add_char[j:j+i]
            results.append(res)

    return results


def fun_test():
    
    # 将字符串切分开
    strs = '回龙观街道东村家园甲10号楼7单元'
    word_list = get_word_list(strs)
    print('输入: {}'.format(strs))
    print('输出: {}'.format(word_list))


if __name__=='__main__':

    # 投递数据
    yuxin_path = 'D:\CPRI\项目6-智能派件\育新投递.csv'
    yuxin = pd.read_csv(yuxin_path)

    # 获取关键词保存到字典的keys中
    gjz = get_keyword(gjz_path=None)
    # print('gjz:{}'.format(gjz))

    results = []

    for index, row in yuxin.iterrows():
        addr = str(row['receiver_addr'])
        print('地址: {}'.format(addr))

        # 根据长度过滤一些异常值
        if len(addr) > 9:
            addr = addr.replace('北京市北京市昌平区', '')

            # 按字切分
            word_list = get_word_list(addr)

            # 根据切分结果进行穷举，并判断是否在关键词字典中
            qj = qiongju(word_list,2,8)
            # print(qj)
            r = None
            for q in qj:
                qq = ''.join(q)
                ck = qq in gjz.keys()
                if ck:
                    r = qq
                # print('{}: {}'.format(qq, ck))
            print('关键词: {}'.format(r))

        else:
            r = 'pass'
            print(r)

        result = [addr,r]
        results.append(result)
            
    result_df = pd.DataFrame(data=results, columns=['add', 'res'])
    savepath = 'project/zhinengpaijian/results.txt'
    result_df.to_csv(savepath, sep='\t',index=True, header = True)
    print(result_df)