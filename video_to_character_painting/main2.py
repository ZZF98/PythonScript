from threading import Thread

from PIL import Image as im
from tkinter import *
import cv2

# 随便打
# codeLib = '''@B%8*hkLft-hj!+:,^. '''
codeLib = " .,-'`:!1+*abcdefghijklmnopqrstuvwxyz<>()\/{}[]?234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ%&@#$"
count = len(codeLib)
import invoke


def play_audio(video_path):
    # https: // sourceforge.net / projects / mpv - player - windows / files /
    def call():
        s = invoke.run(f"mpv --no-video {video_path}", hide=True, warn=True)

    # 这里创建子线程来执行音乐播放指令，因为 invoke.run() 是一个阻塞的方法，要同时播放字符画和音乐的话，就要用多线程/进程。
    # P.S. 更新：现在发现可以用 subprocess.Popen 实现异步调用 mpv，不需要开新线程。有兴趣的同学可以自己试试。
    p = Thread(target=call)
    p.setDaemon(True)
    p.start()


def transform(image_file):
    codePic = ''
    for h in range(0, image_file.size[1]):
        for w in range(0, image_file.size[0]):
            g, r, b = image_file.getpixel((w, h))
            gray = int(r * 0.299 + g * 0.587 + b * 0.114)
            codePic = codePic + codeLib[int(((count - 1) * gray) / 256)]
        codePic = codePic + '\r\n'
    return codePic


def image2char(image_file):
    image_file = image_file.resize((int(image_file.size[0] * 0.16), int(image_file.size[1] * 0.06)))  # 调整图片大小
    return transform(image_file), image_file.size[0], image_file.size[1]


def frame2image(cap, i):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    _, b = cap.read()
    image = im.fromarray(cv2.cvtColor(b, cv2.COLOR_BGR2RGB))
    return image


def gui(path):
    cap = cv2.VideoCapture(path)
    root = Tk()
    t = frame2image(cap, 0)
    _, w, h = image2char(t)
    text = Text(root, width=w, height=h)
    text.pack()
    framenum = int(cap.get(7))
    flag = 1
    for i in range(framenum):
        if flag == 1:
            play_audio(path)
            flag = flag + 2
        image = frame2image(cap, i)
        content, _, _ = image2char(image)
        text.insert(INSERT, content)
        root.update()
        text.delete(0.0, END)


if __name__ == '__main__':
    gui(
        'https://vdept.bdstatic.com/7864465077526a57534656385743576e/5479554765734d6b/1af4093184cf26e3966c66a4da5e76d2a75db50635a79fa2ad0c95124233d3ffb899a19d81670f6b2e1000bd67baa392.mp4?auth_key=1593113278-0-0-5102c04dec81bdd912365d751bb5305a')
