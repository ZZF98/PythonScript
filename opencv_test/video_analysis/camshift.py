# 连续自适应均值漂移
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(
    'https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
# 以视频的第一帧为例
ret, frame = cap.read()
# 设置窗口的初始位置
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
        # 应用camshift获取新位置
        ret, track_window = cv.CamShift(dst, track_window, term_crit)
        # 画在图像上
        pts = cv.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv.polylines(frame, [pts], True, 255, 2)
        cv.imshow('img2', img2)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break
