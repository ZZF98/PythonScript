# 背景消减法
"""
背景减法(BS)是一种使用静态相机生成前景掩码(即包含场景中移动物体像素的二值图像)的常用技术。
顾名思义，BS计算前景遮罩，执行当前帧和背景模型之间的减法，
包含场景的静态部分，或者更一般地说，考虑到所观察场景的特征，所有可以被视为背景的部分。
背景建模主要包括两个步骤:
背景初始化;
背景更新。
"""
from __future__ import print_function

import argparse

import cv2 as cv

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.',
                    default='../C90842500_2019_10_16_15_00_09.mp4')
# D:\PythonScript\opencv_test\C90842500_2019_10_16_15_00_09.mp4
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
# 创建背景减法器对象
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
# 对象用于读取输入的视频或图像序列
capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    # 每一帧都用于计算前景掩码和更新背景
    # 如果想更改用于更新背景模型的学习率，可以通过向apply方法传递一个参数来设置特定的学习率。
    fgMask = backSub.apply(frame)
    # 获取帧号并将其写入当前帧
    cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    # 显示当前帧和fg蒙版
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
