
# 

import yaml

a = [['name','lc'], ['age', 18.01234]]
b = {}

for i in a:
    b[i[0]] = i[1]

b['new'] = '%.4f'%(0.2345677)
save_name = 'dict.yaml'

with open(save_name, 'w') as f:
    f.write(yaml.dump(b, allow_unicode=True))