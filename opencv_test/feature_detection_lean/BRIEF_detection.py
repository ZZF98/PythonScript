import cv2 as cv

img = cv.imread('a.jpg', 0)
# 启动快速检测器
star = cv.xfeatures2d.StarDetector_create()
# 启动 BRIEF 提取器
brief = cv.xfeatures2d.BriefDescriptorExtractor_create()
# 找到关键点
kp = star.detect(img, None)
# 用BRIEF计算描述符
kp, des = brief.compute(img, kp)
print(brief.descriptorSize())
print(des.shape)
img3 = cv.drawKeypoints(img, kp, None, color=(255, 0, 0))
cv.imshow("a", img3)
key = cv.waitKey(0) & 0xFF
# 按'q'健退出循环
if key == ord('q'):
    cv.destroyAllWindows()
