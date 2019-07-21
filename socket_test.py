# import socket

# 查看当前主机名
#
# print('当前主机名称为 : ' + socket.gethostname())
#
# # 根据主机名称获取当前IP
# print('当前主机的IP为: ' + socket.gethostbyname(socket.gethostname()))
#
# # Mac下上述方法均返回127.0.0.1
# # 通过使用socket中的getaddrinfo中的函数获取真真的IP
#
# # 下方代码为获取当前主机IPV4 和IPV6的所有IP地址(所有系统均通用)
# addrs = socket.getaddrinfo(socket.gethostname(), None)
#
# for item in addrs:
#     print(item)
#
# # 仅获取当前IPV4地址
# print('当前主机IPV4地址为:' + [item[4][0] for item in addrs if ':' not in item[4][0]][0])
#
# # 同上仅获取当前IPV4地址
# for item in addrs:
#     if ':' not in item[4][0]:
#         print('当前主机IPV4地址为:' + item[4][0])
#         break

from scapy.all import *
from scapy.layers.inet import ICMP, IP

for i in range(100):
    # 生成目标IP
    ip = "192.168.31." + str(i)
    # 打印生成的目标IP
    print("=目标ip为=>", ip)
    # 根据目标IP组包, ICMP可以看做Ping
    p = IP(dst=ip) / ICMP()
    # 将数据包发出, 等待0.5秒,无回应则放弃等待
    r = sr1(p, timeout=0.5)
