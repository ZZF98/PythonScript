# Harris角点检测
import cv2 as cv
import numpy as np

"""
OpenCV has the function cv.cornerHarris() for this purpose. Its arguments are :

img - 输入图像，应该是灰度和浮点32型.
blockSize - 它是用于角落检测的邻域大小
ksize -采用Sobel导数的孔径参数。
k - 哈里斯探测器方程中的自由参数
"""

filename = "timg.jpg"
# filename = "../opencv_lean/c.jpg"
img = cv.imread(filename)
# 转为灰度图
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('gray', gray)
gray = np.float32(gray)
dst = cv.cornerHarris(gray, 2, 3, 0.04)
# 扩大了标记的角落
dst = cv.dilate(dst, None)
# 阈值为一个最优值，它可以根据图像的不同而变化
img[dst > 0.01 * dst.max()] = [0, 0, 255]
cv.imshow('dst', img)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()

# cv.cornerSubPix()，它进一步细化了以亚像素精度检测到的角
"""
先找到哈里斯角。然后我们通过这些角的质心(可能在一个角上有一堆像素，我们取它们的质心)来细化它们。Harris角用红色像素标记，精制角用绿色像素标记。
"""
filename = "timg2.jpg"
img = cv.imread(filename)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 寻找 Harris角点
gray = np.float32(gray)
dst = cv.cornerHarris(gray, 2, 3, 0.001)
dst = cv.dilate(dst, None)
# 去除噪声，即过滤掉太小或太大的像素值
ret, dst = cv.threshold(dst, 0.01 * dst.max(), 255, 0)
dst = np.uint8(dst)
# 寻找重心
ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
# 定义停止和细化角落的标准
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.04)
# 该函数迭代求出角点或径向鞍点的亚像素精确位置
corners = cv.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
# Now draw them
res = np.hstack((centroids, corners))
res = np.int0(res)
img[res[:, 1], res[:, 0]] = [0, 0, 255]
img[res[:, 3], res[:, 2]] = [0, 255, 0]
cv.imwrite('timg_subpixel.png', img)
cv.imshow('dst', img)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
