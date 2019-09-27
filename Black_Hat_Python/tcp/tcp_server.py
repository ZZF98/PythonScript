#!/usr/bin/python
# coding=utf-8
# tcp服务端
import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print('[*] Listening on %s:%d' % (bind_ip, bind_port))


# 客户处理线程
def handle_client(client_socket):
    # 打印客户端发送得到的消息
    request = client_socket.recv(1024)

    print("[*] Received: %s" % request.decode())

    # 返回一个数据包
    client_socket.send("ACK!".encode())

    client_socket.close()


while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

    # 挂起客户端线程，处理传入数据
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
