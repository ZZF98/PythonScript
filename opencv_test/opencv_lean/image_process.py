import cv2 as cv

# 读取图片
# cv.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
# cv.IMREAD_GRAYSCALE : Loads image in grayscale mode
# cv.IMREAD_UNCHANGED : Loads image as such including alpha channel
img = cv.imread('a.jpg', cv.IMREAD_GRAYSCALE)

# 显示图片
# 可调整大小
cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow("image", img)
# 如果输入0 无限期等待
key = cv.waitKey(0) & 0xFF
print(key)
if key == ord('q'):
    # 删除所有窗口
    cv.destroyAllWindows()

# 保存图片
cv.imwrite("b.jpg", img)
