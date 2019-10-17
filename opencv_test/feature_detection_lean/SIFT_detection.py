# SIFT算法
"""
主要分四步：
1.尺度空间极值检测
2.关键点的定位
3.方向分配
4.关键点描述
5.特征点匹配
"""

"""
AttributeError: module 'cv2.cv2' has no attribute 'xfeatures2d'
pip uninstall opencv-python
pip install opencv_python==3.4.2.16 
pip install opencv-contrib-python==3.4.2.16
"""
import cv2 as cv

img = cv.imread('timg.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
sift = cv.xfeatures2d.SIFT_create()

"""
detect
查找图像中的关键点。如果只搜索图像的一部分，可以传递模板。
每个关键点是一个特殊的结构，它有许多属性，比如它的(x,y)坐标，有意义的邻域的大小，
指定其方向的角度，指定关键点强度的响应等等。
"""
kp = sift.detect(gray, None)
"""
drawKeypoints
该函数在关键点的位置上绘制小圆圈
DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS:它会绘制一个大小为keypoint的圆，甚至会显示它的方向。参见下面的例子。
img=cv.drawKeypoints(gray,kp,img,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv.imwrite('sift_keypoints.jpg',img)
"""
img = cv.drawKeypoints(gray, kp, img)
cv.imshow('s', img)

kp, des = sift.compute(gray, kp)
cv.imshow('des', des)

kp2, des2 = sift.detectAndCompute(gray, None)
cv.imshow('des2', des2)

if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()

"""
现在，为了计算描述符，OpenCV提供了两个方法。
sift.compute():既然已经找到了关键字，那么可以调用sift.compute()，它根据找到的关键字计算描述符。例如:kp,des = sift.compute(gray,kp)
sift.detectAndCompute():如果没有找到关键字，可以使用函数sift.detectAndCompute()在单个步骤中直接找到关键字和描述符。
sift = cv.xfeatures2d.SIFT_create()
kp, des = sift.detectAndCompute(gray,None)
这里kp是一个关键点列表，des是一个数组NumKeypointsber_of_×128的数字数组。
"""
