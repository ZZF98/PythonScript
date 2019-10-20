# 模糊图像
"""
与一维信号一样，图像也可以用各种低通滤波器(LPF)、
高通滤波器(HPF)等进行滤波。LPF有助于去除噪音，
模糊图像等。HPF过滤器有助于在图像中找到边缘。
"""
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# 二维卷积(图像滤波)
img = cv.imread('a.jpg')
kernel = np.ones((5, 5), np.float32) / 25
dst = cv.filter2D(img, -1, kernel)
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(dst), plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()

# 图像模糊(图像平滑)
# 取平均值
img = cv.imread('a.jpg')
blur = cv.blur(img, (5, 5))
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(blur), plt.title('Blurred')
plt.xticks([]), plt.yticks([])
plt.show()

# 高斯模糊
img = cv.imread('a.jpg')
blur = cv.GaussianBlur(img, (5, 5), 0)
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(blur), plt.title('Gaussian')
plt.xticks([]), plt.yticks([])
plt.show()

# 模糊中值
img = cv.imread('a.jpg')
blur = cv.medianBlur(img, 5)
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(blur), plt.title('Median')
plt.xticks([]), plt.yticks([])
plt.show()

# 双边滤波
img = cv.imread('a.jpg')
blur = cv.bilateralFilter(img, 9, 75, 75)
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(blur), plt.title('Bilateral')
plt.xticks([]), plt.yticks([])
plt.show()
