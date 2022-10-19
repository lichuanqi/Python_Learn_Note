import re
import sys
import time
from matplotlib.pyplot import get

import pandas as pd


def get_keyword(gjz_path) -> dict:
    """
    读取关键字列表
    Args: 
        gjz_path: 育新关键字表.xls文件路径
    Return:
        gjz: 
    """
    gjz_path = 'D:\CPRI\项目6-智能派件\data_gjz.xls'
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


def get_shixian() -> dict:
    """
    读取时限数据表
    Args:
        shixian:
    Return:
        dict
    """
    shixian_dict = {}
    shixian_path = 'D:\CPRI\项目6-智能派件\data_shixian.xlsx'
    shixian = pd.read_excel(shixian_path)
    # print(shixian)

    for index,row in shixian.iterrows():
        k = row[0] + '_' + row[1]
        v = row[2]

        shixian_dict[k] = v

    return shixian_dict


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


def add_juhedian(toudi_path, savepath):
    '''
    根据投递表的地址信息计算聚合点,并增加到表中
    Args
        toudi_path: 投递表路径
        savepath: 新的投递表保存路径
    Return
        True
    '''
    # 读取投递数据
    toudi = pd.read_csv(toudi_path, sep='\t')
    print(toudi)

    # 获取关键词保存到字典的keys中
    gjz = get_keyword(gjz_path=None)

    juhedian = []
    for index, row in toudi.iterrows():
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

        juhedian.append(r)

    # 将聚合点数据单独保存为文件
    # result_df = pd.DataFrame(data=results, columns=['add', 'res'])
    # savepath = 'project/zhinengpaijian/results.txt'
    # result_df.to_csv(savepath, sep='\t',index=True, header = True)
    # print(result_df)

    # 将聚合点数据增加一列到投递表
    toudi.insert(14,column='juhedian', value=juhedian)
    toudi.to_csv(savepath, sep='\t',index=True, header = True)

    return True


def add_pinci(toudi_path, savepath):
    """
    根据投递表的地址信息计算投递频次,并增加到表中
        下段时间12:00前,时限要求当日,可1频、2频投
        下段时间12:00前,时限要求当频,1频投
        下段时间12:00后,2频投
    Args
        toudi_path: 投递表路径
        savepath: 新的投递表保存路径
    Return
        True
    """
    # 读取投递数据
    toudi = pd.read_csv(toudi_path)
    # print(toudi)

    # 读取时限数据表到字典
    # 时限要求有两种：当日、当频
    shixian_dict = get_shixian()
    # print(shixian_dict)

    # 读取下段时间、邮件类型、时限要求
    pincis = []
    for index, row in toudi.iterrows():

        leixing1 = '速递'
        leixing2 = str(row['business_prodduct_name'])

        leixing = leixing1 + '_' + leixing2
        shixian = shixian_dict[leixing]

        time_xiaduan = str(row['first_xiaduan'])
        if '/' in time_xiaduan:
            time_xiaduan_h = int(time_xiaduan.split(' ')[1].split(':')[0])
        else:
            time_xiaduan_h = 25
        # print('下段时间: {},邮件类型: {},时限要求: {}'.format(time_xiaduan_h,leixing,shixian))

        # 根据以上三个信息计算投递频次
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

        print('下段时间: {},邮件类型: {},时限要求: {},频次: {}'. \
                format(time_xiaduan_h,leixing,shixian, pinci))
    
    # 数据增加一列到投递表
    toudi.insert(14,column='pinci', value=pincis)
    toudi.to_csv(savepath, index=True, header = True)


def fun_test():
    # 将字符串切分开
    strs = '回龙观街道东村家园甲10号楼7单元'
    word_list = get_word_list(strs)
    print('输入: {}'.format(strs))
    print('输出: {}'.format(word_list))


if __name__=='__main__':
    # toudi_path = 'D:\CPRI\项目6-智能派件\data_toudi_utf-8.txt'
    # savepath = 'project/zhinengpaijian/youdi_juhedian.txt'
    # add_juhedian(toudi_path, savepath)

    toudi_path = 'D:\CPRI\项目6-智能派件\育新投递.csv'
    savepath = 'project/zhinengpaijian/toudi_pinci.csv'
    add_pinci(toudi_path, savepath)