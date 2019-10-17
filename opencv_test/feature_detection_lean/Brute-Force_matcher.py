import cv2 as cv
import matplotlib.pyplot as plt

# ORB Descriptors
img1 = cv.imread('a.jpg', cv.IMREAD_GRAYSCALE)  # queryImage
img2 = cv.imread('a.jpg', cv.IMREAD_GRAYSCALE)  # trainImage
# orb探测器
orb = cv.ORB_create()
# 使用ORB查找关键点和描述符
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

"""
One of NORM_L1, NORM_L2, NORM_HAMMING, NORM_HAMMING2. 
L1 and L2 norms are preferable choices for SIFT and SURF descriptors, 
L1和L2规范是SIFT和SURF描述符更好的选择，
NORM_HAMMING应与ORB搭配使用，既轻快又简短
"""
# 创建BFMatcher对象
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
# 描述符匹配
"""
使用Matcher.match()方法获得两个图像的最佳匹配。
我们将它们按照距离的升序进行排序，以便最好的匹配(较低的距离)出现在前面。
然后我们只抽到前10场比赛(只是为了让大家看到。)你可以随意增加)
DMatch.distance -描述符之间的距离。越低越好。
DMatch.trainIdx - 描述符中描述符的索引
DMatch.queryIdx -查询描述符中的描述符的索引
DMatch.imgIdx - 图像的索引。
"""
matches = bf.match(des1, des2)
# 按它们的距离排序
matches = sorted(matches, key=lambda x: x.distance)
# Draw first 10 matches.
img3 = cv.drawMatches(img1, kp1, img2, kp2, matches[:100], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv.imshow('test', img3)
# cv.imwrite('test.jpg', img3)
plt.imshow(img3), plt.show()
key = cv.waitKey(0) & 0xFF
# 按'q'健退出循环
if key == ord('q'):
    cv.destroyAllWindows()

# 用SIFT描述符进行穷举匹配和比值检验

# 启动 SIFT 探测器
sift = cv.xfeatures2d.SIFT_create()
# 使用SIFT查找关键点和描述符
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
# 具有默认参数的BFMatcher
bf = cv.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
# 应用比值判别法
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])
# cv.drawMatchesKnn 将两个列表进行匹配
img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv.imshow('test', img3)
plt.imshow(img3), plt.show()
key = cv.waitKey(0) & 0xFF
# 按'q'健退出循环
if key == ord('q'):
    cv.destroyAllWindows()
