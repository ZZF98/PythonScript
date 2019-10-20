# 形态变换

import cv2 as cv
import numpy as np

"""
它有助于去除小的白色噪声
"""
# 侵蚀
img = cv.imread('a.jpg', 0)
cv.imshow('img', img)
kernel = np.ones((5, 5), np.uint8)
erosion = cv.erode(img, kernel, iterations=1)
cv.imshow('erode', erosion)

"""
通常，在去除噪音的情况下，腐蚀之后是膨胀。
因为，侵蚀消除了白噪音，但它也缩小了我们的对象。
我们把它放大。由于噪声消失了，它们就不会回来了，
但是我们的目标区域增加了。它在连接一个物体破碎的部分时也很有用。
"""
# 膨胀
img = cv.imread('a.jpg', 0)
kernel = np.ones((5, 5), np.uint8)
dilation = cv.dilate(img, kernel, iterations=1)
cv.imshow('dilate', dilation)

"""
开放只是侵蚀的另一个名称，紧随其后的是扩张。
如上所述，它在去除噪声方面很有用。
"""
# 扩张
img = cv.imread('b.png', 0)
kernel = np.ones((5, 5), np.uint8)
opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
cv.imshow('opening', opening)

"""
闭合与打开相反，扩张之后是侵蚀。
它在关闭前景对象内部的小孔或对象上的小黑点时非常有用。
"""
# 闭合
img = cv.imread('a.png', 0)
kernel = np.ones((5, 5), np.uint8)
closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
cv.imshow('closing', closing)

"""
图像的膨胀和腐蚀的区别。
结果看起来就像对象的轮廓。
"""
# 形态梯度
img = cv.imread('a.png', 0)
kernel = np.ones((5, 5), np.uint8)
gradient = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)
cv.imshow('gradient', gradient)

"""
它是输入图像和打开图像之间的区别。
"""
# Top Hat
img = cv.imread('a.png', 0)
kernel = np.ones((5, 5), np.uint8)
tophat = cv.morphologyEx(img, cv.MORPH_TOPHAT, kernel)
cv.imshow('tophat', tophat)

"""
它是输入图像的闭合和输入图像闭合的区别。
"""
# Black Hat
img = cv.imread('a.png', 0)
kernel = np.ones((5, 5), np.uint8)
blackhat = cv.morphologyEx(img, cv.MORPH_BLACKHAT, kernel)
cv.imshow('blackhat', blackhat)

k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()
