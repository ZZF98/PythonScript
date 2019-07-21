# import psutil
#
#
# # 获取网卡名称和其ip地址，不包括回环
# def get_netcard():
#     netcard_info = []
#     info = psutil.net_if_addrs()
#     for k, v in info.items():
#         for item in v:
#             if item[0] == 2 and not item[1] == '127.0.0.1':
#                 netcard_info.append((k, item[1]))
#     return netcard_info
#
#
# if __name__ == '__main__':
#     print(get_netcard())


import socket
import threading

routers = []
lock = threading.Lock()


def search_routers():
    routers = []
    local_ips = socket.gethostbyname_ex(socket.gethostname())[2]  # get local IP
    all_threads = []
    for ip in local_ips:
        for i in range(1, 255):
            array = ip.split('.')
            array[3] = str(i)
            new_ip = '.'.join(array)
            t = threading.Thread(target=check_ip, args=(new_ip,))
            t.start()
            all_threads.append(t)
    for t in all_threads:
        t.join()

    return local_ips


def check_ip(new_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((new_ip, 80))
    s.close()
    if result == 0:
        lock.acquire()
        print
        new_ip.ljust(15), ' port 80 is open'
        routers.append((new_ip, 80))
        lock.release()


ip_list = search_routers()

import subprocess as sp

# ip = ['192.168.31.1']
ip = ip_list
ip = ['192.168.31.1', '192.168.56.1', '192.168.99.1', '192.168.23.1', '192.168.234.1']
good = 0
bad = 0
count = 0
badIp = []
ipList = []
for url in ip:
    for i in range(1, 255):
        array = url.split('.')
        array[3] = str(i)
        new_ip = '.'.join(array)
        status, result = sp.getstatusoutput("ping " + new_ip)
        # status, result = sp.getstatusoutput("ping " + new_ip + " -w 2")
        count += 1
        if "请求超时" in result:
            bad += 1
            badIp.append(new_ip)
        else:
            ipList.append(new_ip)
            good += 1
print(badIp)
print(ipList)
print('总共ping了 %d条ip' % (count))
print('其中%d条有问题' % (bad))
print('%d条没问题' % (good))
print('坏ip是:')
print(badIp)
