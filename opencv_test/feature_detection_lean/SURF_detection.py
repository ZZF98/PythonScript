"""
SURF增加了很多功能来提高每一步的速度。分析表明，它比SIFT快3倍，性能与SIFT相当。
SURF擅长处理模糊和旋转的图像，但不擅长处理视角变化和光照变化
"""
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('a.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
surf = cv.xfeatures2d.SURF_create(400)
# 计算原始关键的个数
kp, des = surf.detectAndCompute(img, None)
ss = cv.drawKeypoints(img, kp, None, (255, 0, 0))
cv.imshow('ss', ss)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()

print("当前关键点个数：{}".format(len(kp)))
# 检查当前海森阈值
print(surf.getHessianThreshold())

# 修改后显示关键点个数
# 我们把它定在50000左右。它只是用来表示图像的。
# 在实际情况中，值最好是300-500
surf.setHessianThreshold(50000)
kp, des = surf.detectAndCompute(img, None)
print("设置阈值后当前关键点个数：{}".format(len(kp)))
# img = cv.drawKeypoints(gray, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img2 = cv.drawKeypoints(img, kp, None, (255, 0, 0), 4)
cv.imshow('s', img2)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()

# 检查直立标志
# 去除方向后显示
print(surf.getUpright())
surf.setUpright(True)
kp, des = surf.detectAndCompute(img, None)
img3 = cv.drawKeypoints(img, kp, None, (255, 0, 0), 4)
cv.imshow('img3', img3)
plt.imshow(img2), plt.show()
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()


# 打印描述符的大小
print(surf.descriptorSize())
# extended为false
print(surf.getExtended())
surf.setExtended(True)
kp, des = surf.detectAndCompute(img, None)
print(surf.descriptorSize())
img4 = cv.drawKeypoints(img, kp, None, (255, 0, 0), 4)
cv.imshow('img4', img4)
k = cv.waitKey(0) & 0xFF
if k == ord('q'):
    cv.destroyAllWindows()
