import time

import cv2
import numpy as np

camera = cv2.VideoCapture("rtmp://rtmp01open.ys7.com/openlive/4924a5ef58e84be49f6722d50ed68224.hd")  # 参数0表示第一个摄像头
# camera = cv2.VideoCapture("rtmp://rtmp01open.ys7.com/openlive/f91a803c64ad4a38ba697903b63e32b6.hd")  # 参数0表示第一个摄像头
# camera = cv2.VideoCapture("C90843783_1570650823000_23_68907616224.MP4")  # 参数0表示第一个摄像头
# 判断视频是否打开
if (camera.isOpened()):
    print('Open')
else:
    print('摄像头未打开')

# 测试用,查看视频size
size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('size:' + repr(size))

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
kernel = np.ones((5, 5), np.uint8)
background = None
sum = 0
pre_count = 0

while True:
    # 读取视频流
    grabbed, frame_lwpCV = camera.read()
    # 对帧进行预处理，先转灰度图，再进行高斯滤波。
    # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
    gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
    gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)

    # 将第一帧设置为整个输入的背景
    if background is None:
        background = gray_lwpCV
        continue
    # 对于每个从背景之后读取的帧都会计算其与北京之间的差异，并得到一个差分图（different map）。
    # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
    diff = cv2.absdiff(background, gray_lwpCV)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]  # 二值化阈值处理
    diff = cv2.dilate(diff, es, iterations=2)  # 形态学膨胀

    # 显示矩形框
    contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓
    if len(contours) == 0 or len(contours) <= pre_count + 3 or pre_count - 3 <= len(contours):
        # if len(contours) == pre_count or len(contours) == 0:
        sum = sum + 1
        print(sum)
    else:
        pre_count = len(contours)
        sum = 0
    cv2.imshow("a", diff)
    cv2.imshow("b", background)
    cv2.imshow("c", gray_lwpCV)
    cv2.imshow("d", frame_lwpCV)
    # cv2.accumulateWeighted(diff, background, 0.6, gray_lwpCV)
    for c in contours:
        if cv2.contourArea(c) < 1700:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
            continue
        (x, y, w, h) = cv2.boundingRect(c)  # 该函数计算矩形的边界框
        # 过滤时间 640/50

        if x > 1190 and x < 1190 + 640 and y > 42 and y < 60 + 42:
            continue
        cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.rectangle(frame_lwpCV, (1190, 42), (1190 + 640, 42 + 60), (0, 255, 0), 2)

    if sum == 0:
        file_name = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        cv2.imwrite(file_name + ".jpg", frame_lwpCV)

    if sum >= 50:
        print("更新background-------{}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
        gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)
        background = gray_lwpCV
        sum = 0

    cv2.imshow('contours', frame_lwpCV)
    cv2.imshow('dis', diff)
    key = cv2.waitKey(1) & 0xFF
    # 按'q'健退出循环
    if key == ord('q'):
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()
