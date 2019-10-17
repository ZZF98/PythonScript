import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('../opencv_lean/c.jpg', 0)
# 启动ORB检测器
orb = cv.ORB_create()
# 使用ORB查找关键点
kp = orb.detect(img, None)
# 使用ORB计算描述符
kp, des = orb.compute(img, kp)
# 只绘制关键点的位置，而不是大小和方向
img2 = cv.drawKeypoints(img, kp, None, color=(0, 255, 0), flags=0)
plt.imshow(img2), plt.show()
cv.imshow("a", img2)
key = cv.waitKey(0) & 0xFF
# 按'q'健退出循环
if key == ord('q'):
    cv.destroyAllWindows()
