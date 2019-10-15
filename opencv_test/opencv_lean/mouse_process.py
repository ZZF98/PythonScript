import cv2 as cv
import numpy as np

# 所有可用鼠标事件
events = [i for i in dir(cv) if 'EVENT' in i]
print(events)

img = np.zeros((512, 512, 3), np.uint8)


# 鼠标回调函数
def draw_circle(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(img, (x, y), 10, (255, 0, 0), -1)


def demo1():
    # Create a black image, a window and bind the function to window
    cv.namedWindow('image')
    cv.setMouseCallback('image', draw_circle)
    while True:
        cv.imshow('image', img)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()


# demo2
drawing = False  # true if mouse is pressed
mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1


# mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
            else:
                cv.circle(img, (x, y), 5, (0, 0, 255), -1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
        else:
            cv.circle(img, (x, y), 5, (0, 0, 255), -1)


cv.namedWindow('image')
cv.setMouseCallback('image', draw_circle)
while True:
    cv.imshow('image', img)
    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == ord('q'):
        break
cv.destroyAllWindows()
