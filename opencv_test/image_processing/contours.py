# 轮廓
"""
寻找轮廓就像从黑色背景中寻找白色物体。
记住，要找的对象应该是白色的，背景应该是黑色的。
"""
import cv2 as cv
import numpy as np

img = cv.imread('apple.jpg')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)
"""
findcontour()函数中有三个参数，第一个是源图像，
第二个是轮廓检索模式，第三个是轮廓逼近方法。
输出轮廓和层次结构。轮廓是图像中所有轮廓的Python列表。
每个单独的轮廓是一个(x,y)坐标的Numpy数组的边界点的对象。

CV_CHAIN_CODE - Freeman 链码的输出轮廓. 其它方法输出多边形(定点序列). 
CV_CHAIN_APPROX_NONE - 将所有点由链码形式翻译(转化）为点序列形式 
CV_CHAIN_APPROX_SIMPLE - 压缩水平、垂直和对角分割，即函数只保留末端的象素点; 
CV_CHAIN_APPROX_TC89_L1, 
CV_CHAIN_APPROX_TC89_KCOS - 应用 Teh-Chin 链逼近算法. CV_LINK_RUNS - 通过连接为 1 的水平碎片使用完全不同的轮廓提取算法。仅有 CV_RETR_LIST 提取模式可以在本方法中应用. 
"""
cv.imshow('img', img)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# 绘制图像中的所有轮廓:
cv.drawContours(img, contours, -1, (0, 255, 0), 3)
cv.imshow('img1', img)
# 要画一个单独的轮廓，比如第四个轮廓:
cv.drawContours(img, contours, 1, (0, 255, 0), 3)
cv.imshow('img2', img)
# :画一个单独的轮廓，最后两种方法是相同的
cnt = contours[4]
cv.drawContours(img, [cnt], 0, (0, 255, 0), 3)
cv.imshow('img3', img)

# 轮廓形状特征
"""
图像矩可以帮助你计算一些特征，如物体的质心，物体的面积等。
"""
img = cv.imread('d.jpg', 2)
img2 = cv.imread('d.jpg')
ret, thresh = cv.threshold(img, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, 1, 2)
cv.imshow('org', img2)
cnt = contours[2]
# Moments
M = cv.moments(cnt)
print(M)
# 轮廓面积
area = cv.contourArea(cnt)
print(area)
# 轮廓周长
perimeter = cv.arcLength(cnt, True)
print(perimeter)
# 轮廓逼近
epsilon = 0.1 * cv.arcLength(cnt, True)
cv.imshow('epsilon', epsilon)
approx = cv.approxPolyDP(cnt, epsilon, True)
cv.imshow('approx', epsilon)
# 任意方向矩形
rect = cv.minAreaRect(cnt)
box = cv.boxPoints(rect)
box = np.int0(box)
cv.drawContours(img2, [box], 0, (255, 255, 0), 3)
cv.imshow('boxPoints', img2)
# 圆
(x, y), radius = cv.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
cv.circle(img2, center, radius, (255, 255, 0), 2)
cv.imshow('circle', img2)
# 线
rows, cols = img.shape[:2]
[vx, vy, x, y] = cv.fitLine(cnt, cv.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x * vy / vx) + y)
righty = int(((cols - x) * vy / vx) + y)
cv.line(img2, (cols - 1, righty), (0, lefty), (255, 255, 0), 2)
cv.imshow('line', img2)
k = cv.waitKey(3000) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()

# 轮廓属性
# 屏幕高宽比
x, y, w, h = cv.boundingRect(cnt)
aspect_ratio = float(w) / h
print(aspect_ratio)
# 大小
area = cv.contourArea(cnt)
x, y, w, h = cv.boundingRect(cnt)
rect_area = w * h
extent = float(area) / rect_area
print(extent)
# 体积
area = cv.contourArea(cnt)
hull = cv.convexHull(cnt)
hull_area = cv.contourArea(hull)
solidity = float(area) / hull_area
print(solidity)
# 直径
area = cv.contourArea(cnt)
equi_diameter = np.sqrt(4 * area / np.pi)
# 方向
(x, y), (MA, ma), angle = cv.fitEllipse(cnt)
# 掩模和像素点
mask = np.zeros(imgray.shape, np.uint8)
cv.drawContours(mask, [cnt], 0, 255, -1)
pixelpoints = np.transpose(np.nonzero(mask))
# pixelpoints = cv.findNonZero(mask)
# 最大值、最小值及其位置
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(imgray, mask=mask)
# 平均颜色或平均强度
# mean_val = cv.mean(im, mask=mask)
# 极值点
leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])


