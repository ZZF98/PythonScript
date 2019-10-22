# 图像中提取前景
"""
cv.grabCut():
img - 输入图像
mask - 这是一个遮罩图像，我们指定哪些区域是背景，前景或可能的背景/前景等。
它是由以下标志，cv.GC_BGD,cv.GC_FGD,cv.GC_PR_BGD,cv.GC_PR_FGD，或简单地将0,1,2,3传递给图像。
rect - 它是一个矩形的坐标，其中包括格式为(x,y,w,h)的前景对象。
bdgModel, fgdModel - 这些是算法内部使用的数组。你只需要创建两个np。类型为大小为(1,65)的零数组。
迭代次数——算法应该运行的迭代次数。
mode - 应该是cv.GC_INIT_WITH_RECT或cv.GC_INIT_WITH_MASK或组合它决定我们是绘制矩形还是最终的润色笔画。
"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('meixi.jpg')
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = (50, 50, 450, 290)
cv.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img * mask2[:, :, np.newaxis]
plt.imshow(img), plt.colorbar(), plt.show()

# newmask is the mask image I manually labelled
newmask = cv.imread('meixi_s.jpg', 0)
# wherever it is marked white (sure foreground), change mask=1
# wherever it is marked black (sure background), change mask=0
mask[newmask == 0] = 0
mask[newmask == 255] = 1
mask, bgdModel, fgdModel = cv.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_MASK)
mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img * mask[:, :, np.newaxis]
plt.imshow(img), plt.colorbar(), plt.show()
