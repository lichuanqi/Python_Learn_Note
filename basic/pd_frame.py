import pandas as pd


basic_info_list = [
              ['001', '张三', '2018'],
              ['002', '李四', '2014'],
              ['003', '王五', '2020'],
              ['004', '赵六', '2011']]

score_list = [
         ['001', '90', '80', '70'],
         ['002', '80', '70', '60'],
         ['003', '70', '60', '50'],
         ['006', '60', '50', '40']]

basic_info_df = pd.DataFrame(data=basic_info_list, columns=['id', 'name', 'year'])
score_df = pd.DataFrame(data=score_list, columns=['id', 'math', 'english', 'chinese'])

score_df['overall'] = score_df['math'].map(int) + score_df['english'].map(int) + score_df['chinese'].map(int)

# 根据行标签和列标签定位某个值
print(basic_info_df.loc[:,'name'])

# 合并两个表
merge = pd.merge(basic_info_df, score_df, how='left', on='id')

print('basic_info_df\n', basic_info_df)
print('score_df\n', score_df)
print('merge\n', merge)