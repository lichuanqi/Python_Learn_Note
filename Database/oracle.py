import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir="C:/Users/lc/Downloads/instantclient-basic-windows.x64-19.17.0.0.0dbru/instantclient_19_17")

# 连接
ora_username = 'system'
ora_passward = '123456'
ora_address = '192.168.35.221:1524/ORCLCDB'
connection = cx_Oracle.connect(ora_username,ora_passward,ora_address,encoding="UTF-8")
cursor = connection.cursor()

# 新建表
sql = """
     CREATE TABLE student (
     id number primary key,
     name varchar2(30),
     age number,
     daepartment varchar2(30)
     )"""
try:
    cursor.execute(sql)
    connection.commit()
    print("新建表完成")
except:
    print('表已存在')

# # 插入数据
# sql2 = """insert into student values('100006','赵六','24','顺丰')"""
# cursor.execute(sql2)

# sql1 = """insert into student values(:id,:name,:age,:daepartment)"""
# param = [(100007,'张三',19, '北京工业大学')]
# param1 = [(100008,'李四',20, '北京交通大学'),
#           (100009,'王五',21, '中国邮政')]
# cursor.executemany(sql1,param)
# cursor.executemany(sql1,param1)
# connection.commit()
# print("插入数据完成")

# 查询数据
sql3 = """select * from student"""
s = cursor.execute(sql3)
print("查询数据完成")
print(s.fetchmany(3))

# 通配符查询
sql = """SELECT * FROM student WHERE daepartment LIKE '%北%工%大%'"""
s = cursor.execute(sql)
print("查询数据完成")
print(s.fetchmany(3))

# 当确定不在使用连接时，可以使用connection.close()关闭连接
cursor.close()
connection.close()