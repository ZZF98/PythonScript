# 相机校正
import glob

import cv2 as cv
import numpy as np

"""
可以使用vc.cornerSubPix()来提高它们的准确性。我们还可以使用cv.drawChessboardCorners()来绘制模式。
"""
# 中止条件
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# 准备对象分,像(0,0,0),(1,0,0),(2,0,0).... (6 5 0)
objp = np.zeros((6 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
# 数组，用于存储来自所有图像的对象点和图像点。
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
images = glob.glob('*.jpg')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 找到棋盘的角落
    ret, corners = cv.findChessboardCorners(gray, (7, 6), None)
    # 如果找到，添加对象点、图像点(细化后)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        # 绘制和显示角落
        cv.drawChessboardCorners(img, (7, 6), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
        # 校准
        """
        有了目标点和图像点，我们准备进行校准。
        我们可以使用函数cf.calibrateCamera()来返回摄像机矩阵、畸变系数、旋转和平移向量等。
        """
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        print(cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None))

        # 还原
        """
        OpenCV有两种方法可以做到这一点
        但是,首先,我们可以使用vc.getOptimalNewCameraMatrix()根据自由缩放参数细化相机矩阵
        如果缩放参数alpha=0，它将返回具有最小无用像素的未失真图像
        因此，它甚至可能会删除图像角落的一些像素
        如果alpha=1，所有像素都保留一些额外的黑色图像
        该函数还返回一个图像ROI可用于裁剪结果
        """
        img = cv.imread('a.jpg')
        h, w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        # 方法一： 这是最简单的方法。只需调用该函数并使用上面获得的ROI来裁剪结果。
        # dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        # # 裁剪
        # x, y, w, h = roi
        # dst = dst[y:y + h, x:x + w]
        # cv.imshow('calibresult.png', dst)

        # 方法二： 使用重新映射
        mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        cv.imwrite('calibresult2.png', dst)
        cv.waitKey(0)
cv.destroyAllWindows()
np.savez('B', cv.imread("../image_processing/apple.jpg"))
