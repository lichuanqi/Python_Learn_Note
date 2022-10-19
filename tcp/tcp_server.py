# 在Python中创建一个tcp服务器

import socket


if __name__ == '__main__':
    # 创建tcp服务端套接字,参数同客户端配置一致
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    # 设置端口号复用，让程序退出端口号立即释放，否则的话在30秒-2分钟之内这个端口是不会被释放的，这是TCP的为了保证传输可靠性的机制。
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
   
    # 给客户端绑定端口号，客户端需要知道服务器的端口号才能进行建立连接。IP地址不用设置，默认就为本机的IP地址。
    tcp_server.bind(("", 61234))
   
    # 设置监听
    # 128:最大等待建立连接的个数， 提示： 目前是单任务的服务端，同一时刻只能服务与一个客户端，后续使用多任务能够让服务端同时服务与多个客户端
    # 不需要让客户端进行等待建立连接
    # listen后的这个套接字只负责接收客户端连接请求，不能收发消息，收发消息使用返回的这个新套接字tcp_client来完成
    tcp_server.listen(128)
   
    # 等待客户端建立连接的请求, 只有客户端和服务端建立连接成功代码才会解阻塞，代码才能继续往下执行
    # 1. 专门和客户端通信的套接字： tcp_client
    # 2. 客户端的ip地址和端口号： tcp_client_address
    tcp_client, tcp_client_address= tcp_server.accept()
    
    # 代码执行到此说明连接建立成功
    print("客户端的ip地址和端口号:", tcp_client_address)
   
    # 接收客户端发送的数据, 这次接收数据的最大字节数是1024
    recv_data = tcp_client.recv(1024)
   
    # 对服务器发来的数据进行解码保存到变量recv_content中
    recv_content = recv_data.decode(encoding = "utf-8")
    print("接收客户端的数据为:", recv_content)
    
    # 准备要发送给服务器的数据
    send_data = "好的，消息已收到".encode(encoding = "utf-8")
   
    # 发送数据给客户端
    tcp_client.send(send_data)
   
    # 关闭服务与客户端的套接字， 终止和客户端通信的服务
    tcp_client.close()
   
    # 关闭服务端的套接字, 终止和客户端提供建立连接请求的服务 但是正常来说服务器的套接字是不需要关闭的，因为服务器需要一直运行。
    # tcp_server.close()

