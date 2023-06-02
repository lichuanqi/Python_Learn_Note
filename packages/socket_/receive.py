# encoding: utf-8
# 监听端口收到的信息

def send_process(input_s='FF 03 00 09 00 08 81 D0'):
    input_s = input_s.strip()
    send_list = []
    while input_s != '':
        num = int(input_s[0:2], 16)
        input_s = input_s[2:].strip()
        send_list.append(num)
    input_s = bytes(send_list)

    return input_s

import socket
import time

# 创建一个socket套接字，该套接字还没有建立连接
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定监听端口，这里必须填本机的IP192.168.27.238，localhost和127.0.0.1是本机之间的进程通信使用的
server.bind(('172.16.252.56', 8081))
# 开始监听，并设置最大连接数
server.listen(5)

print(u'waiting for connect...')
# 等待连接，一旦有客户端连接后，返回一个建立了连接后的套接字和连接的客户端的IP和端口元组
connect, (host, port) = server.accept()
print(u'the client %s:%s has connected.' % (host, port))

# 接受客户端的数据
# data = connect.recv(1024)

while host:
    # 发送数据给客户端
    connect.sendall(b'\xff\x03\x00\t\x00\x08\x81\xd0')

    # 接受数据
    data = connect.recv(1024)
    data = bytes(data)
    
    out_s = ''
    for i in range(0,len(data)):
        out_s = out_s + ' ' + str(data[i])
    out_s = out_s.split(' ')
    data = out_s
    
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(time_now + ' Receive: ' + str(data))
    print('len:' + str(len(data)))
    print('温度：{:.2f}：摄氏度'.format((int(data[4])*256+int(data[5]))/100-40))
    print('湿度：{}%'.format((int(data[6])*256+int(data[7]))/100))
    print('压强：{}hPa'.format((int(data[8])*256+int(data[9]))/10))
    print('风速：{}m/s'.format((int(data[10]) * 256 + int(data[11]))/100))
    print('风向：{}度'.format((int(data[12]) * 256 + int(data[13]))/10))
    print('雨量：{}mm/min'.format((int(data[14]) * 256 + int(data[15]))/10))
    print('辐射：{}W/m^2'.format((int(data[16]) * 256 + int(data[17]))))
    print('光照：{}Lux'.format((int(data[18]) * 256 + int(data[19]))*10))

    time.sleep(20)

# 结束socket
server.close()