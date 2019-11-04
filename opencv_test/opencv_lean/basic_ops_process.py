import cv2 as cv
from matplotlib import pyplot as plt

# pip install opencv-python
# 编辑图像处理
img = cv.imread('a.jpg')
# 行/列 返回BGR
px = img[100, 290]
print(px)
px = img[100, 10]
print(px)
px = img[136, 153]
print(px)
# 设置像素
img[118, 140] = [0, 0, 255]
img[140, 169] = [0, 0, 255]
cv.imshow("a", img)
# 行/列/通道数
# 如果是灰度图只有行和列
print(img.shape)
print(img.size)
print(img.dtype)
eye = img[118:140, 140:169]
img[138:160, 160:189] = eye
cv.imshow("b", img)
# 分割/合并图片
b, g, r = cv.split(img)
img = cv.merge((b, g, r))
if cv.waitKey(0) == ord('q'):
    cv.destroyAllWindows()

BLUE = [255, 0, 0]
img1 = cv.imread('a.jpg')
replicate = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_REPLICATE)
reflect = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_REFLECT)
reflect101 = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_REFLECT_101)
wrap = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_WRAP)
constant = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_CONSTANT, value=BLUE)
plt.subplot(231), plt.imshow(img1, 'gray'), plt.title('ORIGINAL')
plt.subplot(232), plt.imshow(replicate, 'gray'), plt.title('REPLICATE')
plt.subplot(233), plt.imshow(reflect, 'gray'), plt.title('REFLECT')
plt.subplot(234), plt.imshow(reflect101, 'gray'), plt.title('REFLECT_101')
plt.subplot(235), plt.imshow(wrap, 'gray'), plt.title('WRAP')
plt.subplot(236), plt.imshow(constant, 'gray'), plt.title('CONSTANT')
plt.show()
if cv.waitKey(0) == ord('q'):
    cv.destroyAllWindows()
