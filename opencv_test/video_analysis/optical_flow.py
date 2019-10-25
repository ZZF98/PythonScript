# 光流法
"""
光流是由物体或摄像机的运动引起的图像对象在两个连续帧之间的视运动模式。
它是一个二维向量场，其中每个向量都是一个位移向量，表示点从第一帧到第二帧的移动。
"""
import threading

import cv2 as cv
import numpy as np


# Lucas-Kanade光流
def Lucas_Kanade():
    cap = cv.VideoCapture(
        "https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4")
    # 为ShiTomasi角落检测参数
    feature_params = dict(maxCorners=100,
                          qualityLevel=0.3,
                          minDistance=7,
                          blockSize=7)
    # lucas kanade光流的参数
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    # 创建一些随机的颜色
    color = np.random.randint(0, 255, (100, 3))
    # 拿第一帧，在里面找角
    ret, old_frame = cap.read()
    old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
    p0 = cv.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    # 创建一个掩模图像用于绘图
    mask = np.zeros_like(old_frame)
    while True:
        ret, frame = cap.read()
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # 计算光流
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        # 选择好点
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        # 画出痕迹
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv.line(mask, (a, b), (c, d), color[i].tolist(), 2)
            frame = cv.circle(frame, (a, b), 5, color[i].tolist(), -1)
        img = cv.add(frame, mask)
        cv.imshow('frame', img)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        # 现在更新前面的帧和前面的点
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)


# OpenCV中的密集光流
def Dense_Optical_Flow():
    # cap = cv.VideoCapture(cv.samples.findFile("https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4"))
    cap = cv.VideoCapture(
        "https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4")
    ret, frame1 = cap.read()
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255
    while True:
        ret, frame2 = cap.read()
        next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        cv.imshow('frame2', bgr)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv.imwrite('opticalfb.png', frame2)
            cv.imwrite('opticalhsv.png', bgr)
        prvs = next


# 方法一：
# Lucas_Kanade()
# # 方法二：
# Dense_Optical_Flow()
try:
    t1 = threading.Thread(target=Lucas_Kanade)
    t2 = threading.Thread(target=Dense_Optical_Flow)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
except Exception as e:
    print("Error: 无法启动线程")
    pass
