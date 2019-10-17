# Shi-Tomasi角落探测器,更适合跟踪
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

filename = "../opencv_lean/c.jpg"
img = cv.imread(filename)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 25表示找到25个最好的角
corners = cv.goodFeaturesToTrack(gray, 6, 0.01, 10)
corners = np.int0(corners)
for i in corners:
    x, y = i.ravel()
    cv.circle(img, (x, y), 3, 255, -1)
plt.imshow(img), plt.show()
