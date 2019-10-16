import cv2 as cv

img1 = cv.imread('b.jpg')
img2 = cv.imread('c.jpg')
# 图片合成
dst = cv.addWeighted(img1, 0.5, img2, 0.5, 0)
cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()

# 图片覆盖
img1 = cv.imread('b.jpg')
img2 = cv.imread('a.jpg')
# 居中
rows, cols, channels = img2.shape
rows1, cols1, channels1 = img1.shape
roi = img1[round((rows1 - rows) / 2):rows + round((rows1 - rows) / 2),
      round((cols1 - cols) / 2):cols + round((cols1 - cols) / 2)]
# 创建掩码
img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)
cv.imshow('mask_inv', mask_inv)
cv.waitKey(0)
cv.destroyAllWindows()

# 将roi区域置为黑
img1_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
cv.imshow('res_1', img1_bg)
cv.waitKey(0)
cv.destroyAllWindows()

# 从标识图像中只提取标识的区域
img2_fg = cv.bitwise_and(img2, img2, mask=mask)
cv.imshow('res_2', img2_fg)
cv.waitKey(0)
cv.destroyAllWindows()

# 将logo放入ROI中，修改主图
dst = cv.add(img1_bg, img2_fg)
cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()

img1[round((rows1 - rows) / 2):rows + round((rows1 - rows) / 2),
round((cols1 - cols) / 2):cols + round((cols1 - cols) / 2)] = dst
cv.imshow('res', img1)
cv.waitKey(0)
cv.destroyAllWindows()
