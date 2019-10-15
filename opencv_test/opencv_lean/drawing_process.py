import cv2 as cv
import numpy as np

# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
# 线
cv.line(img, (0, 0), (511, 511), (255, 0, 0), 5)
cv.imwrite("line.jpg", img)
# 正方形
cv.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)
cv.imwrite("rectangle.jpg", img)
# 圆
cv.circle(img, (447, 63), 63, (0, 0, 255), -1)
cv.imwrite("circle.jpg", img)
# 椭圆
cv.ellipse(img, (256, 256), (100, 50), 0, 0, 360, 255, -1)
cv.imwrite("ellipse.jpg", img)
# 多边形
pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv.polylines(img, [pts], True, (0, 255, 255))
cv.imwrite("polylines.jpg", img)
# 添加文字
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img, 'emm', (10, 500), font, 4, (255, 255, 255), 2, cv.LINE_AA)
cv.imwrite("font.jpg", img)
