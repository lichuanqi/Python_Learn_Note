import socket
import threading
import time


def dispose_client_request(tcp_client_1,tcp_client_address):
    """
    循环接收和发送数据
    """
    while True:
        recv_data = tcp_client_1.recv(4096)
        # 6 有消息就回复数据，消息长度为0就是说明客户端下线了
        if recv_data:
            print(f"客户端发来的消息是: {recv_data}")
            send_read = b"\xaa\xaa\xaa\x01\xb1\x00\x00\x1a"
            tcp_client_1.sendall(send_read)
            print(f'发送数据: {send_read}')

            time.sleep(5)
            print('静默结束，开始下次发送数据')
        else:
            print(f'客户端下线了: {tcp_client_address[1]}')
            tcp_client_1.close()
            break

def get_zhongliang_thread(tcp_client_1,tcp_client_address):
    """
    循环读取和接受重量传感器数据
    """
    while True:
        send_read_data = b"\xaa\xaa\xaa\x01\xb1\x00\x00\x1a"
        tcp_client_1.sendall(send_read_data)
        print(f'SEND 已发送命令: {send_read_data}')

        recv_data = tcp_client_1.recv(4096)

        if len(recv_data) >= 6:
            print(f'收到原始数据: {recv_data}')
            zl, dw = get_data_bytes(recv_data)
            print(f'转换得到的重量数据: {zl} ({dw})')
        else:
            print('收到心跳包数据')

        time.sleep(5)
        print('静默结束，开始下次发送数据')

def get_data_bytes(data):
    """
    根据微重力传感器传回的字节计算重量
    Arg
        data [bytes]: 微重力传感器传回的字节数据,如下格式
              \xbb\xbb\xbb\x01\xb1\x21\x34\x04\x03\x0b
    Return
        zhongliang [float]: 重量数值
        danwei [str]: 单位，['Mpa', 'Kg', 'T']
    """
    if not isinstance(data,bytes):
        raise BaseException('请检查数据类型是否为 bytes')

    dots = [1, 10, 100, 1000]
    danweis = ['Mpa', 'Kg', 'T']

    out_s = ''
    for i in range(0,len(data)):
        out_s = out_s + ' ' + str(data[i]) 
    out_s = out_s.strip().split(' ')

    h16 = '0x' + str(hex(int(out_s[5])))[2:] + str(hex(int(out_s[6])))[2:]
    print(f'h16: {h16}')
    data = int(h16, 16)
    xiaoshudian = dots[int(out_s[7])-1]
    zhongliang = data / xiaoshudian
    danwei = danweis[int(out_s[8])-1]
    
    return zhongliang, danwei

if __name__ == '__main__':

    # 1 创建服务端套接字对象
    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
  
    # 2 绑定端口,开始监听
    listen_ip = '192.168.35.221'
    listen_port = 9000
    tcp_server.bind((listen_ip,listen_port))
    tcp_server.listen(128)
    print(f'开始监听: ({listen_ip},{listen_port})')
    
    tcp_client_1 , tcp_client_address = tcp_server.accept()
    print(f"连接到客户端: {tcp_client_address}")

    while True:
        send_read_data = b"\xaa\xaa\xaa\x01\xb1\x00\x00\x1a"
        tcp_client_1.sendall(send_read_data)
        print(f'SEND 已发送命令: {send_read_data}')

        recv_data = tcp_client_1.recv(4096)

        if len(recv_data) >= 6:
            print(f'收到原始数据: {recv_data}')
            zl, dw = get_data_bytes(recv_data)
            print(f'转换得到的重量数据: {zl} ({dw})')
        else:
            print('收到心跳包数据')

        time.sleep(5)
        print('静默结束，开始下次发送数据')

    # 4 循环等待客户端连接请求（也就是最多可以同时有128个用户连接到服务器进行通信）
    # while True:
        # tcp_client_1 , tcp_client_address = tcp_server.accept()
        # print(f"连接到客户端: {tcp_client_address}")

        # 每次连接到客户端时新建一个线程
        # thd = threading.Thread(target = dispose_client_request, args = (tcp_client_1,tcp_client_address))
        # 设置守护主线程  即如果主线程结束了 那子线程中也都销毁了  防止主线程无法退出
        # thd.setDaemon(True)
        # 启动子线程对象
        # thd.start()