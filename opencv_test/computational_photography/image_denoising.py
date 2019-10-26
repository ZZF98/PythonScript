# 图像去噪
"""
Image Denoising in OpenCV
OpenCV provides four variations of this technique.

cv.fastNlMeansDenoising() - 处理单一灰度图像
cv.fastNlMeansDenoisingColored() - 与彩色图像一起工作。
cv.fastNlMeansDenoisingMulti() - 处理短时间内捕获的图像序列(灰度图像)
cv.fastNlMeansDenoisingColoredMulti() - 和上面一样，但是是彩色的。
常见的参数是:
h:决定过滤强度的参数。较高的h值可以更好地去除噪声，但也可以去除图像的细节。(10就可以了)
hForColorComponents:与h相同，但仅用于彩色图像。(通常与h相同)
templateWindowSize:应该是奇数。(7)建议
searchWindowSize:应该是奇数。(推荐21)
"""
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# cv.fastNlMeansDenoisingColored()
img = cv.imread('a.jpg')
dst = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
plt.subplot(121), plt.imshow(img)
plt.subplot(122), plt.imshow(dst)
plt.show()

# cv.fastNlMeansDenoisingMulti()
cap = cv.VideoCapture('rtmp://202.69.69.180:443/webcast/bshdlive-pc')
# 创建一个前5帧的列表
img = [cap.read()[1] for i in range(5)]
# 转换所有的灰度
gray = [cv.cvtColor(i, cv.COLOR_BGR2GRAY) for i in img]
# 将所有数据转换为float64
gray = [np.float64(i) for i in gray]
# 制造一个变化的噪音
noise = np.random.randn(*gray[1].shape) * 10
# 将此噪声添加到图像中
noisy = [i + noise for i in gray]
# 转换回uint8
noisy = [np.uint8(np.clip(i, 0, 255)) for i in noisy]
# 考虑到所有的5帧，去噪第三帧
dst = cv.fastNlMeansDenoisingMulti(noisy, 2, 5, None, 4, 7, 35)
plt.subplot(131), plt.imshow(gray[2], 'gray')
plt.subplot(132), plt.imshow(noisy[2], 'gray')
plt.subplot(133), plt.imshow(dst, 'gray')
plt.show()
