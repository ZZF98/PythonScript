import json
import os

from tool.email_send import SendMail

dir = 'C:\\Users\\EDZ\\Desktop\\模拟推出\\windows-多路录像测试长跑版-64位-20190923\\'
exe = 'SmartStreamRelayTool.exe'
config = 'conf\\nt_app_relay_stream_entity_conf.json'


def main():
    while True:
        r_v = os.system(dir + exe)
        if r_v == 20:
            # 打开一个json文件
            data = open(dir + config, encoding='utf-8')
            # 转换为python对象
            strJson = json.load(data)
            rtmp_number = len(strJson["relay_stream_entity"])
            for i in range(1, rtmp_number + 1):
                print(strJson["relay_stream_entity"])

            # # 开始录制
            # mouse_click(777, 286)
            # mouse_click(862, 287)
        print(r_v)
        # 发送短信
        m = SendMail(
            username='XXXXX@QQ.com',
            passwd='CCCCCCCCCCCCCCCCC',
            recv=['CCCCCCCCCCC@QQ.com'],
            title='视频流中断',
            content='中断',
            file=r'smart_sdk.log',
            ssl=True,
        )
        m.send_mail()


if __name__ == '__main__':
    main()
