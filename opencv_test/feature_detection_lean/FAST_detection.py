"""
它比其他现有的角落探测器快几倍。
但它对高水平的噪音并不强壮。它依赖于一个阈值。
"""
import cv2 as cv

"""
cv.FAST_FEATURE_DETECTOR_TYPE_5_8
cv.FAST_FEATURE_DETECTOR_TYPE_7_12 
cv.FAST_FEATURE_DETECTOR_TYPE_9_16
fast = cv.FastFeatureDetector_create(cv.FAST_FEATURE_DETECTOR_TYPE_9_16)
"""

img = cv.imread('a.jpg', 0)
# 使用默认值初始化快速对象
fast = cv.FastFeatureDetector_create()
# 找到并画出关键点
kp = fast.detect(img, None)
img2 = cv.drawKeypoints(img, kp, None, color=(255, 0, 0))
print("关键点个数:{}".format(len(kp)))
# 打印所有默认参数
print("Threshold: {}".format(fast.getThreshold()))
print("nonmaxSuppression:{}".format(fast.getNonmaxSuppression()))
print("neighborhood: {}".format(fast.getType()))
print("Total Keypoints with nonmaxSuppression: {}".format(len(kp)))
cv.imshow('fast_true', img2)
# 禁用nonmaxSuppression
fast.setNonmaxSuppression(0)
kp = fast.detect(img, None)
print("关键点个数:{}".format(len(kp)))
print("Total Keypoints without nonmaxSuppression: {}".format(len(kp)))
img3 = cv.drawKeypoints(img, kp, None, color=(255, 0, 0))
cv.imshow('fast_false', img3)
key = cv.waitKey(0) & 0xFF
# 按'q'健退出循环
if key == ord('q'):
    cv.destroyAllWindows()
