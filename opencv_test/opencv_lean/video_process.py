import cv2 as cv


def play():
    cap = cv.VideoCapture("rtmp://202.69.69.180:443/webcast/bshdlive-pc")
    # 获取宽度高度
    print(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    print(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    # 设置宽度高度
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 2048)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1024)
    if not cap.isOpened():
        print("无法打开视频流")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # 判断帧是否被正常读取
        if not ret:
            print("无法接收帧,退出 ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # 打印显示这一帧

        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


# 保存
def save():
    cap = cv.VideoCapture("rtmp://202.69.69.180:443/webcast/bshdlive-pc")
    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('output.avi', fourcc, 20.0,
                         (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("无法接收帧,退出 ...")
            break
        # 翻转
        # frame = cv.flip(frame, 0)
        # 写入帧
        out.write(frame)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    # 释放资源
    cap.release()
    out.release()
    cv.destroyAllWindows()
