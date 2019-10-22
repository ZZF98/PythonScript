# Hough直线检测
import cv2 as cv
import numpy as np

"""
第一个参数，输入的图像应该是二值图像，所以在应用霍夫变换之前应用阈值或使用canny边缘检测。
第二个和第三个参数分别为ρ和θ的准确性。
第四个参数是阈值，这意味着它应该被视为一条线的最低数。
"""
img = cv.imread(cv.samples.findFile('../feature_detection_lean/timg.jpg'))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150, apertureSize=3)
lines = cv.HoughLines(edges, 1, np.pi / 180, 200)
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv.imshow('houghlines3.jpg', img)

"""
minLineLength - 最小的线长。小于此长度的线段将被拒绝。
maxLineGap - 允许线段之间的最大间隙，将其视为单线。
"""
img = cv.imread(cv.samples.findFile('../feature_detection_lean/timg.jpg'))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150, apertureSize=3)
lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv.imshow('houghlines5.jpg', img)
cv.waitKey(0)
