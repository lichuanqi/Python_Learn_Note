import sqlite3

conn = sqlite3.connect('test.db')
# 创建一个Cursor:
cursor = conn.cursor()

# 执行一条SQL语句，创建user表:
sql_cerate = '''create table box_state(
    id integer primary key,
    time varchar(20),
    image_path varchar(50),
    box_num_in varchar(20),
    ox_num_out varchar(20),
    state_in varchar(20),
    state_out varchar(20))
    '''
cursor.execute(sql_cerate)
 
# 继续执行一条SQL语句，插入一条记录:
id_ = 1000000
name_ = 'lichuan02'
sql_insert = "insert into user (id, name) values (?, ?)"
cursor.execute(sql_insert, (id_, name_))

# 通过rowcount获得插入的行数:
print(cursor.rowcount)
 
# 关闭Cursor:
cursor.close()
# 提交事务:
conn.commit()
# 关闭Connection:
conn.close()