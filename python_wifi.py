# 扫描wifi和连接
import pywifi
import time
# 保存包中写义的常量
from pywifi import const


def wifi_connect_status():
    """
    判断wifi连接状态
    """
    # 创建一个无线对象
    wifi = pywifi.PyWiFi()

    # 有可能有多个无线网卡,所以指定网卡
    iface = wifi.interfaces()[0]

    # 判断是否连接成功
    if iface.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
        return True
    else:
        return False


def scan_wifi():
    """
    扫描wifi
    :return: 扫描结果对象
    """
    # 扫描wifi
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()  # 扫苗附件wifi
    time.sleep(1)
    baseWifi = iface.scan_results()
    for i in baseWifi:
        # ssid 为wifi名称
        print('wifi扫描结果:{}'.format(i.ssid))
        print('wifi设备MAC地址:{}'.format(i.bssid))
    return baseWifi


def connect_wifi(wifiName, password):
    wifi = pywifi.PyWiFi()  # 创建一个wifi对象
    ifaces = wifi.interfaces()[0]  # 取第一个无限网卡
    print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    time.sleep(3)  # 缓冲3秒

    profile = pywifi.Profile()  # 配置文件
    profile.ssid = wifiName  # wifi名称
    profile.auth = const.AUTH_ALG_OPEN  # 需要密码
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    profile.key = password  # wifi密码

    ifaces.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件

    ifaces.connect(tmp_profile)  # 连接
    time.sleep(5)  # 尝试10秒能否成功连接
    isok = True
    if ifaces.status() == const.IFACE_CONNECTED:
        print("成功连接")
    else:
        print("失败")
    # ifaces.disconnect()  # 断开连接
    time.sleep(1)
    return isok


wifi_connect_status()
scan_wifi()
connect_wifi('wwbnqdfg_5G', 'XXX')
