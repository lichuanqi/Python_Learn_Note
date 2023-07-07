from datetime import datetime


now = datetime.now()
day_index = (now-datetime(now.year,1,1)).days + 1
_, day_batch, _ = now.isocalendar()
print('今天是%s, 是今年的第%s天, 第%s个星期'%(now, day_index, day_batch+1))