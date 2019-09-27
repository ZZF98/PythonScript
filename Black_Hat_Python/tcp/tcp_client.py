# coding=utf-8
# tcp客户端
import socket

target_host = "127.0.0.1"
target_port = 1234

# 建立一个socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接客户端
client.connect((target_host, target_port))

# 发送一些数据
client.send("你好\r\n\r\n".encode('utf-8'))

# 接收一些数据
response = client.recv(4096)

print(response.decode())
