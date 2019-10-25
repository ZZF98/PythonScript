import glob

import cv2 as cv
import numpy as np


# 加载数据
# with np.load('B.npz') as X:
#     mtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]


def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
    img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
    img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
    return img


def draw2(img, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)
    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)
    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)
    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)
    return img


objp = np.zeros((6 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)  # 坐标轴
axis_3d = np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0],  # 渲染立方体
                      [0, 0, -3], [0, 3, -3], [3, 3, -3], [3, 0, -3]])

images = glob.glob("*.jpg")
for fname in images:
    img = cv.imread(fname)
    img_copy = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, (7, 6), None)

    objp = np.zeros((6 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
    # 数组，用于存储来自所有图像的对象点和图像点。
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        _, rvecs, tvecs, inliers = cv.solvePnPRansac(objp, corners, mtx, dist)

        imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)
        imgpts_3d, jac_3d = cv.projectPoints(axis_3d, rvecs, tvecs, mtx, dist)

        img = draw(img, corners, imgpts)
        img_3d = draw2(img_copy, imgpts_3d)
        cv.imshow('img', img)
        cv.imshow('img_3d', img_3d)
        k = cv.waitKey(0) & 0xff
        if k == 's':
            cv.imwrite('res.jpg', img)

cv.destroyAllWindows()
