# 直方图
"""
使用vc.calchist()函数来查找直方图
cv.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
images : 它是uint8或float32类型的源映像。它应该用方括号表示，即“[img]”
channels : 它也用方括号表示。它是我们计算直方图的通道的索引
例如，如果输入为灰度图像，则其值为[0]。对于彩色图像，可以通过[0]、[1]、[2]分别计算蓝、绿、红通道的直方图。
mask : 为了求出整幅图像的直方图，将直方图赋值为“None”。但是如果你想找到图像特定区域的直方图，你必须为此创建一个掩码图像并将其作为掩码。
histSize : 他代表我们的bin数。需要用方括号表示。对于完整的规模，我们通过[256]。
ranges : 这是我们的范围。通常是[0,256]。
"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# 简单地加载一个图像在灰度模式，并找到其完整的直方图。
img = cv.imread('apple.jpg', 0)
plt.hist(img.ravel(), 256, [0, 256])
plt.show()

img = cv.imread('orange.jpg')
color = ('b', 'g', 'r')
for i, col in enumerate(color):
    histr = cv.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(histr, color=col)
    plt.xlim([0, 256])
plt.show()

img = cv.imread('apple.jpg', 0)
# create a mask
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:300, 100:400] = 255
masked_img = cv.bitwise_and(img, img, mask=mask)
# Calculate histogram with mask and without mask
# Check third argument for mask
hist_full = cv.calcHist([img], [0], None, [256], [0, 256])
hist_mask = cv.calcHist([img], [0], mask, [256], [0, 256])
plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.imshow(mask, 'gray')
plt.subplot(223), plt.imshow(masked_img, 'gray')
plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
plt.xlim([0, 256])
plt.show()

# 直方图均衡化
img = cv.imread('orange.jpg', 0)
hist, bins = np.histogram(img.flatten(), 256, [0, 256])
cdf = hist.cumsum()
cdf_normalized = cdf * float(hist.max()) / cdf.max()
plt.plot(cdf_normalized, color='b')
plt.hist(img.flatten(), 256, [0, 256], color='r')
plt.xlim([0, 256])
plt.legend(('cdf', 'histogram'), loc='upper left')
plt.show()

# 它的输入是灰度图像，输出是我们的直方图均衡化图像。equalizeHist
img = cv.imread('orange.jpg', 0)
equ = cv.equalizeHist(img)
res = np.hstack((img, equ))  # stacking images side-by-side
cv.imshow('res.png', res)

# 自适应直方图均衡化
img = cv.imread('s.jpg', 0)
# 创建CLAHE对象(参数是可选的)
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
cl1 = clahe.apply(img)
cv.imwrite('clahe_2.jpg', cl1)

img = cv.imread('clahe_2.jpg')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# 绘制图像中的所有轮廓:
cv.drawContours(img, contours, -1, (0, 255, 0), 3)
cv.imshow('clahe_2.jpg', img)

img = cv.imread('s.jpg')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# 绘制图像中的所有轮廓:
cv.drawContours(img, contours, -1, (0, 255, 0), 3)
cv.imshow('s.jpg', img)

cv.waitKey(5000)
cv.destroyAllWindows()

# 2D直方图
"""
2D直方图使用相同的函数cv.calcHist()进行计算。
对于颜色直方图，我们需要将图像从BGR转换为HSV。(记住，对于一维直方图，我们将BGR转换为灰度)。
channels = [0,1] 需要同时处理H和S平面。
bins = [180,256] H平面是180度，S平面是256度。
range = [0,180,0,256]色调值介于0和180之间，饱和度介于0和256之间.
"""
import cv2 as cv

img = cv.imread('apple.jpg')
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
hist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
plt.imshow(hist, interpolation='nearest')
# X轴表示S值，Y轴表示色调。
plt.show()
cv.waitKey(1000)
cv.destroyAllWindows()

# 直方图反向投影
# roi是我们需要寻找的对象或对象区域
roi = cv.imread('apple_s.jpg')
hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
# 目标是我们搜索的图像
target = cv.imread('apple.jpg')
hsvt = cv.cvtColor(target, cv.COLOR_BGR2HSV)
# 使用calcHist查找柱状图,也可以用np.histogram2d
roihist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
# 对直方图进行归一化并应用反向投影
cv.normalize(roihist, roihist, 0, 255, cv.NORM_MINMAX)
dst = cv.calcBackProject([hsvt], [0, 1], roihist, [0, 180, 0, 256], 1)
# Now convolute with circular disc
disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
cv.filter2D(dst, -1, disc, dst)
# 阈值和二进制
ret, thresh = cv.threshold(dst, 50, 255, 0)
thresh = cv.merge((thresh, thresh, thresh))
res = cv.bitwise_and(target, thresh)
res = np.vstack((target, thresh, res))
cv.imshow('res.jpg', res)

cv.waitKey(50000)
cv.destroyAllWindows()

