import sys
import time
from tkinter.messagebox import NO
import pandas as pd


add_path = 'D:\CPRI\项目6-智能派件\育新投递.csv'
df_path = 'D:\CPRI\项目6-智能派件\育新关键字表.xls'
delivery = "D:/CPRI/项目6-智能派件/address.csv"
dtxt = 'D:/CPRI/项目6-智能派件/learn-0-10009612.txt'

# add = pd.read_csv(add_path)
# row_num = len(add)
# print(add)

dlist = []
with open(dtxt, errors='ignore') as f:
    lines = f.readlines()
    for line in lines:
        dlist.append(line.strip().split('||'))
print(len(dlist))
df = pd.DataFrame(dlist, columns=['time','address','jingdu','weidu','num','n'])
print(df)

de_id_df = df['address'].values
de_id_list = df['address'].values.tolist()
de_id_dict_value = df['address'].to_dict()
de_id_dict_key = dict(zip(df['address'].values, df['num'].values))
de_id_set = set(df['address'].values)

print(de_id_df)

time_s = time.time()
for i in range(10000):

    a = '北京北京市昌平区北京市北京市昌平区回龙观龙博苑三区' in de_id_df
    # Time: 40.0137

    a = '北京北京市昌平区北京市北京市昌平区回龙观龙博苑三区' in de_id_list
    # Time: 43.8055

    a = '北京北京市昌平区北京市北京市昌平区回龙观龙博苑三区' in de_id_dict_value
    # Time: 0.001238

    a = '北京北京市昌平区北京市北京市昌平区回龙观龙博苑三区' in de_id_dict_key
    # Time: 0.0009932
    
    a = '北京北京市昌平区北京市北京市昌平区回龙观龙博苑三区' in de_id_set
    # Time: 0.001582

time_e = time.time()
print('用时：{}'.format(time_e-time_s))