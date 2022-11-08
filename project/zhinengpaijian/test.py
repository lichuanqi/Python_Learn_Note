from re import S
import pandas as pd

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def time_test():
    pdt = pd.to_datetime('20220601 00:01', format=r'%Y%m%d %H:%M')
    print(f'pdt: {pdt}')

    pdty = pdt.hour
    print(f'pdfy {pdty}')

def dict_test():

    datas = {}
    data1 = {}

    data1['普邮'] = [{'id': '11111',
                     'lng': 116,
                     'lat': 40},
                     {'id': '11112',
                     'lng': 117,
                     'lat': 41}
    ]

    data1['速递'] = [{'id': '11111',
                    'lng': 116,
                    'lat': 40},
                    {'id': '11112',
                    'lng': 117,
                    'lat': 41}
    ]
    
    datas['点1'] = data1

    print(datas)


def dict_muilt():
    dd = Vividict()
    
    dd['name']['a'] = 1

    print(dd)

    
def count_leixing():

    jh_leixing = {'聚合点1': ['普邮', '普邮', '普邮', '速递'],
                  '聚合点2': ['速递']}

    jh_toudiren = {}
    for key, values in jh_leixing.items():
    # 统计'普邮'和'速递'数量
        jh_lx = {}
        for v in values:
            if v in jh_lx.keys():
                jh_lx[v] += 1
            else:
                jh_lx[v] = 1
            
        jh_toudiren[key] = jh_lx
        
        if '普邮' in jh_toudiren[key].keys():
            jh_toudiren[key]['投递人'] = '普邮'
        else:
            jh_toudiren[key]['投递人'] = '速递' 

    print(jh_toudiren)


def merge_list():
    a = [1,2]
    b = [2,3,4,5]
    c = [1]

    d = [a, b, c]
    print(d)


def for_continue():

    for i in range(10):

        if i%2 == 0:
            
            continue

        print(f'i = {i} 跳出循环')
        
    return True

if __name__ == '__main__':
    for_continue()