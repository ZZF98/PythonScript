# 改变图片颜色
import cv2 as cv
import numpy as np

# BGR→灰度转换，我们使用标志cv.COLOR_BGR2GRAY
flags = [i for i in dir(cv) if i.startswith('COLOR_')]
print(flags)

cap = cv.VideoCapture(0)
while True:
    # 读取每一帧
    _, frame = cap.read()
    # 将BGR转换为HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # 在HSV中定义蓝色范围
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # 阈值HSV图像只得到蓝色
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # 位掩模和原始图像
    res = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)
    k = cv.waitKey(5) & 0xFF
    if k == ord('q'):
        break
cv.destroyAllWindows()
green = np.uint8([[[0, 255, 0]]])
hsv_green = cv.cvtColor(green, cv.COLOR_BGR2HSV)
print(hsv_green)
