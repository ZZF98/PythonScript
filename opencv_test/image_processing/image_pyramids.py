# 图像金字塔
import cv2 as cv

img = cv.imread('a.jpg')
cv.imshow('img', img)
# 高斯金字塔
lower_reso = cv.pyrDown(img)
cv.imshow('a', lower_reso)
# 向下查看图像金字塔。
higher_reso2 = cv.pyrUp(img)
cv.imshow('b', higher_reso2)


# 使用金字塔的图像混合
import cv2 as cv
import numpy as np

A = cv.imread('apple.jpg')
B = cv.imread('orange.jpg')

A = cv.resize(A, (256, 256), cv.INTER_LINEAR)
B = cv.resize(B, (256, 256), cv.INTER_LINEAR)
print(A.shape, B.shape)
# 为A生成高斯金字塔
G = A.copy()
gpA = [G]
for i in range(6):
    G = cv.pyrDown(G)
    # print(G.shape)
    gpA.append(G)
# 为B生成高斯金字塔
G = B.copy()
gpB = [G]  # 将橘子进行高斯金字塔处理，总共六级处理
for i in range(6):
    G = cv.pyrDown(G)
    gpB.append(G)
# 为A生成拉普拉斯金字塔
lpA = [gpA[5]]  # 将苹果进行拉普拉斯金字塔处理，总共5级处理
for i in range(5, 0, -1):
    GE = cv.pyrUp(gpA[i])
    # print(GE.shape)
    # print(gpA[i].shape)
    L = cv.subtract(gpA[i - 1], GE)
    lpA.append(L)
# 为B生成拉普拉斯金字塔
lpB = [gpB[5]]  # 将橘子进行拉普拉斯金字塔处理，总共5级处理
for i in range(5, 0, -1):
    GE = cv.pyrUp(gpB[i])
    L = cv.subtract(gpB[i - 1], GE)
    lpB.append(L)
# 现在在每一层添加图像的左半边和右半边
LS = []
for la, lb in zip(lpA, lpB):
    rows, cols, dpt = la.shape
    # print(la.shape)
    # print(la[:,0:cols//2,:])
    ls = np.hstack((la[:, 0:cols // 2, :], lb[:, cols // 2:, :]))
    LS.append(ls)
# 现在重建
ls_ = LS[0]
for i in range(1, 6):
    ls_ = cv.pyrUp(ls_)
    ls_ = cv.add(ls_, LS[i])
# 图像与直接连接的每一半
real = np.hstack((A[:, :cols // 2, :], B[:, cols // 2:, :]))
cv.imshow('Pyramid_blending', ls_)
cv.imshow('Direct_blending', real)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()
