import cv2 as cv
import numpy as np

img = cv.imread('coins.png')

# 灰度图
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 阈值化
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
cv.imshow('gray', gray)
# 去除噪声
kernel = np.ones((3, 3), np.uint8)
# 侵蚀
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
cv.imshow('opening', opening)
# 确定背景区域
sure_bg = cv.dilate(opening, kernel, iterations=3)
cv.imshow('sure_bg', sure_bg)
# 确定前景区域
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
cv.imshow('dist_transform', dist_transform)
# 发现未知的区域
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)
cv.imshow('unknown', unknown)

# 标记标签
ret, markers = cv.connectedComponents(sure_fg)
# 添加一个到所有标签，使确定的背景不是0，而是1
markers = markers + 1
# 现在，将未知区域标记为0
markers[unknown == 255] = 0
"""
应用分水岭,然后修改标记图像。边界区域将标记为-1
"""
markers = cv.watershed(img, markers)
cv.imshow('markers', img)
img[markers == -1] = [255, 0, 0]
cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()
