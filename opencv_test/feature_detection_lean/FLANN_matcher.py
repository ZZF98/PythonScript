"""
SIFT, SURF:
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
ORB:
FLANN_INDEX_LSH = 6
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2

"""
import cv2 as cv
import matplotlib.pyplot as plt

img1 = cv.imread('a.jpg', cv.IMREAD_GRAYSCALE)  # queryImage
img2 = cv.imread('a.jpg', cv.IMREAD_GRAYSCALE)  # trainImage
# 启动 SIFT 探测器
sift = cv.xfeatures2d.SIFT_create(10000)
# 使用SIFT查找关键点和描述符
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # 或者传递空字典
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)
# 只需要绘制好的匹配，所以创建一个模板
matchesMask = [[0, 0] for i in range(len(matches))]
# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.7 * n.distance:
        matchesMask[i] = [1, 0]
draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=cv.DrawMatchesFlags_DEFAULT)
img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
cv.imshow('test', img3)
# cv.imwrite('test.jpg', img3)
plt.imshow(img3, ), plt.show()
key = cv.waitKey(0) & 0xFF
# 按'q'健退出循环
if key == ord('q'):
    cv.destroyAllWindows()

# 使用ORB
# 启动 SIFT 探测器
orb = cv.ORB_create(10000)
# 使用ORB查找关键点和描述符
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)
# FLANN parameters
FLANN_INDEX_LSH = 6
index_params = dict(algorithm=FLANN_INDEX_LSH,
                    table_number=6,  # 12
                    key_size=12,  # 20
                    multi_probe_level=1)  # 2
search_params = dict()  # 或者传递空字典
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)
# 只需要绘制好的匹配，所以创建一个模板
matchesMask = [[0, 0] for i in range(len(matches))]
# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.7 * n.distance:
        matchesMask[i] = [1, 0]
draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=cv.DrawMatchesFlags_DEFAULT)
img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
cv.imshow('test', img3)
# cv.imwrite('test_orb.jpg', img3)
plt.imshow(img3, ), plt.show()
key = cv.waitKey(0) & 0xFF
# 按'q'健退出循环
if key == ord('q'):
    cv.destroyAllWindows()
