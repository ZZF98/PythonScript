# 轮廓
"""
寻找轮廓就像从黑色背景中寻找白色物体。
记住，要找的对象应该是白色的，背景应该是黑色的。
"""
import cv2 as cv

img = cv.imread('a.png')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)
"""
findcontour()函数中有三个参数，第一个是源图像，
第二个是轮廓检索模式，第三个是轮廓逼近方法。
输出轮廓和层次结构。轮廓是图像中所有轮廓的Python列表。
每个单独的轮廓是一个(x,y)坐标的Numpy数组的边界点的对象。
cv.CHAIN_APPROX_NONE
cv.CHAIN_APPROX_SIMPLE
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
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()


# 轮廓形状特征

