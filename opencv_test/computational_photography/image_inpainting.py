# 图像修复
import cv2 as cv

img = cv.imread('b.jpg')
mask = cv.imread('d.jpg', 0)
dst = cv.inpaint(img, mask, 3, cv.INPAINT_TELEA)
cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()
