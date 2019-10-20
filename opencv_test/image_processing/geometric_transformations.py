# 几何转换
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# cv.resize()缩放
img = cv.imread('a.jpg')
res = cv.resize(img, None, fx=1 / 2, fy=1 / 2, interpolation=cv.INTER_CUBIC)
cv.imshow('a', res)
# OR
height, width = img.shape[:2]
res = cv.resize(img, (2 * width, 2 * height), interpolation=cv.INTER_CUBIC)
cv.imshow('b', res)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()

# cv.warpaffine()平移:第三个参数是输出图像的大小
img = cv.imread('a.jpg', 0)
rows, cols = img.shape
M = np.float32([[1, 0, 50], [0, 1, 50]])
dst = cv.warpAffine(img, M, (cols, rows))
cv.imshow('img', dst)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()

# cv.getRotationMatrix2D旋转
img = cv.imread('a.jpg', 0)
rows, cols = img.shape
# cols-1和rows-1是坐标极限。
M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), 180, 1)
dst = cv.warpAffine(img, M, (cols, rows))
cv.imshow('img', dst)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()

# 仿射变换
img = cv.imread('a.jpg')
rows, cols, ch = img.shape
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
M = cv.getAffineTransform(pts1, pts2)
dst = cv.warpAffine(img, M, (cols, rows))
plt.subplot(121), plt.imshow(img), plt.title('Input')
plt.subplot(122), plt.imshow(dst), plt.title('Output')
plt.show()
cv.imshow('dst', dst)
cv.imshow('img', img)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()

# 透视变换
img = cv.imread('a.jpg')
rows, cols, ch = img.shape
pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
M = cv.getPerspectiveTransform(pts1, pts2)
dst = cv.warpPerspective(img, M, (300, 300))
plt.subplot(121), plt.imshow(img), plt.title('Input')
plt.subplot(122), plt.imshow(dst), plt.title('Output')
plt.show()
cv.imshow('dst', dst)
cv.imshow('img', img)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()
