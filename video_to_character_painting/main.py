# -*- coding:utf-8 -*-
import os
import pickle
import subprocess
import time
from threading import Thread

# 导入 opencv
import cv2
import invoke
# numpy 是一个矩阵运算库，图像处理需要用到。
import numpy as np


# 播放音频，需要下载mpv
def play_audio(video_path):
    # https: // sourceforge.net / projects / mpv - player - windows / files /
    def call():
        invoke.run(f"mpv --no-video {video_path}", hide=True, warn=True)

    # 这里创建子线程来执行音乐播放指令，因为 invoke.run() 是一个阻塞的方法，要同时播放字符画和音乐的话，就要用多线程/进程。
    # P.S. 更新：现在发现可以用 subprocess.Popen 实现异步调用 mpv，不需要开新线程。有兴趣的同学可以自己试试。
    p = Thread(target=call)
    p.setDaemon(True)
    p.start()


# 用于生成字符画的像素，越往后视觉上越明显。。这是我自己按感觉排的，你可以随意调整。
pixels = " .,-'`:!1+*abcdefghijklmnopqrstuvwxyz<>()\/{}[]?234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ%&@#$"


# pixels = " @B%8*hkLft-hj!+:,^. "


# 按帧读取视频
def video2imgs(video_name, size):
    """

    :param video_name: 字符串, 视频文件的路径
    :param size: 二元组，(宽, 高)，用于指定生成的字符画的尺寸
    :return: 一个 img 对象的列表，img对象实际上就是 numpy.ndarray 数组
    """

    img_list = []

    # 从指定文件创建一个VideoCapture对象
    cap = cv2.VideoCapture(video_name)

    # 如果cap对象已经初始化完成了，就返回true，换句话说这是一个 while true 循环
    while cap.isOpened():
        # cap.read() 返回值介绍：
        #   ret 表示是否读取到图像
        #   frame 为图像矩阵，类型为 numpy.ndarry.
        ret, frame = cap.read()
        if ret:
            # 转换成灰度图，也可不做这一步，转换成彩色字符视频。
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # resize 图片，保证图片转换成字符画后，能完整地在命令行中显示。
            img = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)

            # 分帧保存转换结果
            img_list.append(img)
        else:
            break

    # 结束时要释放空间
    cap.release()

    return img_list


# 图像转化为字符画
def img2chars(img):
    """

    :param img: numpy.ndarray, 图像矩阵
    :return: 字符串的列表：图像对应的字符画，其每一行对应图像的一行像素
    """
    res = []

    # 灰度是用8位表示的，最大值为255。
    # 这里将灰度转换到0-1之间
    # 使用 numpy 的逐元素除法加速，这里 numpy 会直接对 img 中的所有元素都除以 255
    percents = img / 255

    # 将灰度值进一步转换到 0 到 (len(pixels) - 1) 之间，这样就和 pixels 里的字符对应起来了
    # 同样使用 numpy 的逐元素算法，然后使用 astype 将元素全部转换成 int 值。
    indexes = (percents * (len(pixels) - 1)).astype(np.int)

    # 要注意这里的顺序和 之前的 size 刚好相反（numpy 的 shape 返回 (行数、列数)）
    height, width = img.shape
    for row in range(height):
        line = ""
        for col in range(width):
            index = indexes[row][col]
            # 添加字符像素（最后面加一个空格，是因为命令行有行距却没几乎有字符间距，用空格当间距）
            line += pixels[index] + " "
        res.append(line)

    return res


def imgs2chars(imgs):
    video_chars = []
    for img in imgs:
        video_chars.append(img2chars(img))

    return video_chars


def play_video(video_chars):
    """
    播放字符视频
    :param video_chars: 字符画的列表，每个元素为一帧
    :return: None
    """
    # 获取字符画的尺寸
    width, height = len(video_chars[0][0]), len(video_chars[0])

    for pic_i in range(len(video_chars)):
        # 显示 pic_i，即第i帧字符画
        for line_i in range(height):
            # 将pic_i的第i行写入第i列。
            print(video_chars[pic_i][line_i])
        time.sleep(1 / 24)  # 粗略地控制播放速度。

        # 调用 shell 命令清屏
        # subprocess.run("clear", shell=True)  # linux 版
        subprocess.run("cls", shell=True)  # cmd 版，windows 系统请用这一行。


def dump(obj, file_name):
    """
    将指定对象，以file_nam为名，保存到本地
    """
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)
    return


def load(filename):
    """
    从当前文件夹的指定文件中load对象
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def get_file_name(file_path):
    """
    从文件路径中提取出不带拓展名的文件名
    """
    # 从文件路径获取文件名 _name
    path, file_name_with_extension = os.path.split(file_path)

    # 拿到文件名前缀
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    return file_name


def has_file(path, file_name):
    """
    判断指定目录下，是否存在某文件
    """
    return file_name in os.listdir(path)


def get_video_chars(video_path, size):
    """
    返回视频对应的字符视频
    """
    video_dump = get_file_name(video_path) + ".pickle"

    # 如果 video_dump 已经存在于当前文件夹，就可以直接读取进来了
    if has_file(".", video_dump):
        print("发现该视频的转换缓存，直接读取")
        video_chars = load(video_dump)
    else:
        print("未发现缓存，开始字符视频转换")

        print("开始逐帧读取")
        # 视频转字符动画
        imgs = video2imgs(video_path, size)

        print("视频已全部转换到图像， 开始逐帧转换为字符画")
        video_chars = imgs2chars(imgs)

        print("转换完成，开始缓存结果")
        # 把转换结果保存下来
        dump(video_chars, video_dump)
        print("缓存完毕")

    return video_chars


# import curses
#
# def play_video(video_chars):
#     """
#     播放字符视频，
#     :param video_chars: 字符画的列表，每个元素为一帧
#     :return: None
#     """
#     # 获取字符画的尺寸
#     width, height = len(video_chars[0][0]), len(video_chars[0])
#
#     # 初始化curses，这个是必须的，直接抄就行
#     stdscr = curses.initscr()
#     curses.start_color()
#     try:
#         # 调整窗口大小，宽度最好略大于字符画宽度。另外注意curses的height和width的顺序
#         stdscr.resize(height, width * 2)
#
#         for pic_i in range(len(video_chars)):
#             # 显示 pic_i，即第i帧字符画
#             for line_i in range(height):
#                 # 将pic_i的第i行写入第i列。(line_i, 0)表示从第i行的开头开始写入。最后一个参数设置字符为白色
#                 stdscr.addstr(line_i, 0, video_chars[pic_i][line_i], curses.COLOR_WHITE)
#             stdscr.refresh()  # 写入后需要refresh才会立即更新界面
#
#             time.sleep(1 / 24)  # 粗略地控制播放速度(24帧/秒)。更精确的方式是使用游戏编程里，精灵的概念
#     finally:
#         # curses 使用前要初始化，用完后无论有没有异常，都要关闭
#         curses.endwin()
#     return
if __name__ == "__main__":
    # 宽，高
    size = (64, 48)
    # 视频路径，换成你自己的
    video_path = "https://vdept.bdstatic.com/7864465077526a57534656385743576e/5479554765734d6b/1af4093184cf26e3966c66a4da5e76d2a75db50635a79fa2ad0c95124233d3ffb899a19d81670f6b2e1000bd67baa392.mp4?auth_key=1593113278-0-0-5102c04dec81bdd912365d751bb5305a"

    # 只转换三十秒，这个属性是才添加的，但是上一篇的代码没有更新。你可能需要先上github看看最新的代码。其实就稍微改了一点。
    seconds = 30

    # 这里的fps是帧率，也就是每秒钟播放的的字符画数。用于和音乐同步。这个更新也没写进上一篇，请上github看看新代码。
    video_chars = get_video_chars(video_path, size)

    # 播放音轨
    play_audio(video_path)

    # 播放视频
    play_video(video_chars)
