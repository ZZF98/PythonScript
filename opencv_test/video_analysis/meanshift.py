# 均值平移算法
"""
假设你有一系列的点。(可以是像直方图反投影那样的像素分布)。
你有一个小窗口(可能是一个圆圈)，你必须把那个窗口移动到最大像素密度的区域(或最大点数)。
通常通过直方图反向投影图像和初始目标位置。当物体运动时，很明显运动反映在直方图背投影图像中。
结果，meanshift算法将我们的窗口移动到密度最大的新位置。
"""

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(
    'https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')

# 以视频的第一帧为例
ret, frame = cap.read()

# 设置窗口的初始位置进入翻译页面
x, y, w, h = 300, 200, 100, 50  # 硬编码了这些值
track_window = (x, y, w, h)

# 设置跟踪ROI
roi = frame[y:y + h, x:x + w]
hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

# 设置终止条件，迭代10次或至少移动1次
term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

while True:
    ret, frame = cap.read()

    if ret:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # 应用meanshift获取新位置
        ret, track_window = cv.meanShift(dst, track_window, term_crit)

        # 画在图像上
        x, y, w, h = track_window
        img2 = cv.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        cv.imshow('img2', img2)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break
