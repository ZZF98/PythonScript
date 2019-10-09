import threading

from ffmpy import FFmpeg


def main(rtmp, url, name):
    ff = FFmpeg(inputs={rtmp: None},
                outputs={url: '-c copy -f flv '})

    print(ff.cmd)
    while True:
        try:
            ff.run()
            print("——————————————————————————————————————————")
            print("rtmp:" + rtmp + " name:" + name)
            print("——————————————————————————————————————————")
        except Exception as e:
            print(e)
            print("——————————————————————————————————————————")
            print("rtmp:" + rtmp + " name:" + name)
            print("——————————————————————————————————————————")


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, rtmp, url, name):
        threading.Thread.__init__(self)
        self.rtmp = rtmp
        self.url = url
        self.name = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        main(self.rtmp, self.url, self.name)


if __name__ == '__main__':
    videoList = [{"rtmp": "rtmp://rtmp01open.ys7.com/openlive/XXXXXXXXXXX.hd",
                  "url": "rtmp://192.168.78.133:1935/zzf/D00269480"},
                 {"rtmp": "rtmp://rtmp01open.ys7.com/openlive/XXXXXXXXXXXCCCCCS.hd",
                  "url": "rtmp://192.168.78.133:1935/zzf/C90843906"}
                 ]
    threadList = []
    for video in videoList:
        threadList.append(myThread(video["rtmp"], video["url"], video["url"].split('/')[-1]))

    # 开启线程
    for thread in threadList:
        thread.start()
