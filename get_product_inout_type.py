# -*- coding:utf-8 -*-

# 从机构功能表中提取 [业务编码] 和 [进出口类型编码]

import sys

import csv
import pandas as pd

flie_path = 'D:\Cpst\项目-省际仿真\省际干线仿真_2022030709\inp_nrc_process_org_param.csv'
save_path = 'D:\Cpst\项目-省际仿真\省际干线仿真_2022030709\inp_nrc_process_org_param_out.csv'

file = pd.read_csv(flie_path)
row_num = len(file)

product_types = {}
product_types_list = []

inout_types = {}
inout_types_list = []

for i in range(0, row_num):
    
    process_org_code = file['process_org_code'][i]
    product_type = file['product_type'][i]
    in_out_type = file['in_out_type'][i]

    # 业务编码
    if process_org_code not in product_types.keys():
        product_types[process_org_code] = [product_type]
    else:
        if product_type not in product_types[process_org_code]:
            product_types[process_org_code].append(product_type)

    # 进出口类型编码
    if process_org_code not in inout_types.keys():
        inout_types[process_org_code] = [in_out_type]
    else:
        if in_out_type not in inout_types[process_org_code]:
            inout_types[process_org_code].append(in_out_type)

# 判断业务编码
for key, value in product_types.items():
    # [1]         1      快包
    # [2]         2      标快 
    # [1,2]    -> 3      快包+标快
    if 1 in value and 2 in value:
        product_types_list.append([key, 3])
    else:
        product_types_list.append([key, int(value[len(value)-1])])

# print('product_types_list\n', product_types_list)
product_types_df = pd.DataFrame(data=product_types_list, 
                                columns=['process_org_code', 'product_type'])
print('product_types_df\n', product_types_df)
# product_types_df.to_csv(save_path,index=False)


# 判断进出口类型编码
for key, value in inout_types.items():
    # [1]         1      进口
    # [2]         2      出口 
    # [3]         3      转口
    # [1,2]    -> 4      进口+出口
    # [1,3]    -> 5      进口+转口
    # [2,3]    -> 6      出口+转口
    # [1,2,3]  -> 7      进口+出口+转口
    if 1 in value and 2 in value and 3 in value:
        inout_types_list.append([key, 7])
    elif 1 in value and 2 in value:
        inout_types_list.append([key, 4])
    elif 1 in value and 3 in value:
        inout_types_list.append([key, 5])
    elif 2 in value and 3 in value:
        inout_types_list.append([key, 6])
    elif 1 in value:
        inout_types_list.append([key, 1])
    elif 2 in value:
        inout_types_list.append([key, 2])
    elif 3 in value:
        inout_types_list.append([key, 3])
    else:
        inout_types_list.append([key, 'Error'])

# print('inout_types_list', inout_types_list)
inout_types_df = pd.DataFrame(data=inout_types_list,
                              columns=['process_org_code', 'in_out_type'])
print('inout_types_df', inout_types_df)
# product_types_df.to_csv(save_path,index=False)

types_merge = pd.merge(product_types_df, inout_types_df)
print('types_merge', types_merge)
types_merge.to_csv(save_path)