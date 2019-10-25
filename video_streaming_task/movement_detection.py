import os
import time

import cv2 as cv


# max为帧差大于15帧
def movement_detection(file, max=15):
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 第几帧
    count = 1
    # 次数
    sum = 0
    max_len = 0
    camera = cv.VideoCapture(file)  # 参数0表示第一个摄像头
    # 判断视频是否打开
    if camera.isOpened():
        print('Open')
        count = count + 1
    else:
        print('摄像头未打开')
        return False
    es = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 4))
    fps = round(camera.get(cv.CAP_PROP_FPS) / 2) - 1
    # 背景图
    background = None
    while True:
        # 读取视频流
        grabbed, frame_lwpCV = camera.read()
        if count % fps == 0 or background is None:
            pass
        else:
            count = count + 1
            continue
        if not grabbed:
            break
        # 对帧进行预处理，先转灰度图，再进行高斯滤波。
        # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
        frame_lwpCV = cv.resize(frame_lwpCV, (500, 500), cv.INTER_LINEAR)
        gray_lwpCV = cv.cvtColor(frame_lwpCV, cv.COLOR_BGR2GRAY)
        gray_lwpCV = cv.GaussianBlur(gray_lwpCV, (21, 21), 0)

        # 将第一帧设置为整个输入的背景
        if background is None:
            background = gray_lwpCV
            continue
        # 对于每个从背景之后读取的帧都会计算其与北京之间的差异，并得到一个差分图（different map）。
        # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
        diff = cv.absdiff(background, gray_lwpCV)
        diff = cv.threshold(diff, 25, 255, cv.THRESH_BINARY)[1]  # 二值化阈值处理
        diff = cv.dilate(diff, es, iterations=2)  # 形态学膨胀
        background = gray_lwpCV
        # 显示矩形框
        contours, hierarchy = cv.findContours(diff.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓

        count_s = 0
        for c in contours:
            # 面积/阈值
            if cv.contourArea(c) < 300:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
                continue
            count_s = count_s + 1

        if count_s > max:
            # 因为光线突然变化
            if len(contours) > 150:
                continue
            file = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            cv.imwrite(str(file) + ".jpg", frame_lwpCV)
            sum = sum + 1
            if max_len < len(contours):
                max_len = len(contours)
            # 累计三次
            if sum > 3:
                max = max_len
                # max = len(contours)
                break
        # cv.imshow('contours', frame_lwpCV)
        # cv.imshow('dis', diff)
        # if len(contours) > max:
        #     print(len(contours))
        # key = cv.waitKey(1) & 0xFF

        count = count + 1
    print(max)
    camera.release()
    cv.destroyAllWindows()
    print(start)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    return False


# max为帧差大于15帧
def movement_detection2(file, max=15):
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    count = 1
    sum = 0
    max_len = 0
    camera = cv.VideoCapture(file)  # 参数0表示第一个摄像头
    # 判断视频是否打开
    if camera.isOpened():
        print('Open')
        count = count + 1
    else:
        print('摄像头未打开')
        return False
    es = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 4))
    fps = round(camera.get(cv.CAP_PROP_FPS) / 2) - 1
    # 背景图
    background = None
    while True:
        # 读取视频流
        grabbed, frame_lwpCV = camera.read()
        if count % fps == 0 or background is None:
            pass
        else:
            count = count + 1
            continue
        if not grabbed:
            break
        # 对帧进行预处理，先转灰度图，再进行高斯滤波。
        # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
        frame_lwpCV = cv.resize(frame_lwpCV, (500, 500), cv.INTER_LINEAR)
        gray_lwpCV = cv.cvtColor(frame_lwpCV, cv.COLOR_BGR2GRAY)
        gray_lwpCV = cv.GaussianBlur(gray_lwpCV, (21, 21), 0)

        # 将第一帧设置为整个输入的背景
        if background is None:
            background = gray_lwpCV
            continue
        # 对于每个从背景之后读取的帧都会计算其与北京之间的差异，并得到一个差分图（different map）。
        # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
        diff = cv.absdiff(background, gray_lwpCV)
        diff = cv.threshold(diff, 25, 255, cv.THRESH_BINARY)[1]  # 二值化阈值处理
        diff = cv.dilate(diff, es, iterations=2)  # 形态学膨胀
        background = gray_lwpCV
        # 显示矩形框
        contours, hierarchy = cv.findContours(diff.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓
        print(len(contours))
        count_s = 0
        for c in contours:
            # 面积/阈值
            if cv.contourArea(c) < 300:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
                continue
            (x, y, w, h) = cv.boundingRect(c)  # 该函数计算矩形的边界框
            count_s = count_s + 1
            cv.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if count_s > max:
            # 因为光线突然变化
            if len(contours) > 150:
                continue
            max = len(contours)
            print(len(contours))
            key = cv.waitKey(5000) & 0xFF
            sum = sum + 1
            if max_len < len(contours):
                max_len = len(contours)
            # 累计三次
            if sum > 3:
                max = max_len
                # max = len(contours)
            # break

        cv.imshow('contours', frame_lwpCV)
        cv.imshow('dis', diff)

        key = cv.waitKey(1) & 0xFF

        count = count + 1
    print(max)
    try:
        camera.release()
        cv.destroyAllWindows()
    except:
        pass
    print(start)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    return False


list_f = os.listdir("video")
for file in list_f:
    print(file)
    movement_detection("video\\" + file, max=3)
    movement_detection2("video\\" + file, max=3)
    break
# movement_detection("D:\\PythonScript\\opencv_test\\C90842500_2019_10_16_15_00_09.mp4", max=15)
