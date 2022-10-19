# 导入套接字模块
import socket
# 导入线程模块
import threading

# 定义个函数,使其专门重复处理客户的请求数据（也就是重复接受一个用户的消息并且重复回答，直到用户选择下线）
def dispose_client_request(tcp_client_1,tcp_client_address):
    # 5 循环接收和发送数据
    while True:
        recv_data = tcp_client_1.recv(4096)
        
        # 6 有消息就回复数据，消息长度为0就是说明客户端下线了
        if recv_data:
            print("客户端是:", tcp_client_address)
            print("客户端发来的消息是:", recv_data.decode())
            send_data = "消息已收到，正在处理中...".encode()
            tcp_client_1.send(send_data)
        else:
            print("%s 客户端下线了..." % tcp_client_address[1])
            tcp_client_1.close()
            break

if __name__ == '__main__':

    # 1 创建服务端套接字对象
    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
  
    # 2 绑定端口
    tcp_server.bind(("",61234))
  
    # 3 设置监听
    tcp_server.listen(128)
  
    # 4 循环等待客户端连接请求（也就是最多可以同时有128个用户连接到服务器进行通信）
    while True:
        tcp_client_1 , tcp_client_address = tcp_server.accept()
        # 创建多线程对象
        thd = threading.Thread(target = dispose_client_request, args = (tcp_client_1,tcp_client_address))
        
        # 设置守护主线程  即如果主线程结束了 那子线程中也都销毁了  防止主线程无法退出
        # thd.setDaemon(True)
        
        # 启动子线程对象
        thd.start()

    # 7 关闭服务器套接字 （其实可以不用关闭，因为服务器一直都需要运行）
    # tcp_server.close()