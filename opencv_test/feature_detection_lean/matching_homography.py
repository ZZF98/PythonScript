import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

MIN_MATCH_COUNT = 10
img1 = cv.imread('a.jpg', 0)  # queryImage
img2 = cv.imread('b.jpg', 0)  # trainImage
# 使用SIFT查找关键点和描述符
sift = cv.xfeatures2d.SIFT_create()
# 使用SIFT查找关键点和描述符
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)
# 根据Lowe's的比率测试，存储所有的匹配项。
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

# 至少有10个匹配项(MIN_MATCH_COUNT定义)用于查找对象
# 否则，只显示一条消息，说明没有足够的匹配项。
# 如果找到了足够的匹配，我们就提取出两个图像中匹配的关键点的位置。
# 它们被传递来寻找补全变换。一旦我们得到了这个3x3的变换矩阵，
# 我们就用它把queryImage的角变换成trainImage中的对应点。然后画出来。
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    # h, w, d = img1.shape
    h, w = img1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv.perspectiveTransform(pts, M)
    img2 = cv.polylines(img2, [np.int32(dst)], True, 255, 3, cv.LINE_AA)


    # 画出图形
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)
    img3 = cv.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
    plt.imshow(img3, 'gray'), plt.show()
    cv.imshow('test', img3)
    # cv.imwrite('test.jpg', img3)
    plt.imshow(img3, ), plt.show()
    key = cv.waitKey(0) & 0xFF
    # 按'q'健退出循环
    if key == ord('q'):
        cv.destroyAllWindows()
else:
    print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
    matchesMask = None
