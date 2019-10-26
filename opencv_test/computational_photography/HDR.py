# 曝光
# 加载曝光图像到一个列表
import cv2 as cv
import numpy as np

# 加载曝光图像到一个列表
img_fn = ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"]
img_list = [cv.imread(fn) for fn in img_fn]
exposure_times = np.array([15.0, 2.5, 0.25, 0.0333], dtype=np.float32)

# 将曝光合并到HDR图像中
merge_debevec = cv.createMergeDebevec()
hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())
merge_robertson = cv.createMergeRobertson()
hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())

# Tonemap HDR图像
tonemap1 = cv.createTonemap(gamma=2.2)
res_debevec = tonemap1.process(hdr_debevec.copy())

# 合并曝光使用Mertens fusion
merge_mertens = cv.createMergeMertens()
res_mertens = merge_mertens.process(img_list)

# 转换为8位并保存
res_debevec_8bit = np.clip(res_debevec * 255, 0, 255).astype('uint8')
res_robertson_8bit = np.clip(res_debevec_8bit * 255, 0, 255).astype('uint8')
res_mertens_8bit = np.clip(res_mertens * 255, 0, 255).astype('uint8')
cv.imwrite("ldr_debevec.jpg", res_debevec_8bit)
cv.imwrite("ldr_robertson.jpg", res_robertson_8bit)
cv.imwrite("fusion_mertens.jpg", res_mertens_8bit)

# 估计相机响应函数(CRF)
"""
相机响应函数(CRF)为我们提供了场景亮度与测量强度值之间的联系。
CRF在包括HDR算法在内的一些计算机视觉算法中具有重要意义。
在这里，我们估计反相机响应函数，并将其用于HDR合并。
"""
cal_debevec = cv.createCalibrateDebevec()
crf_debevec = cal_debevec.process(img_list, times=exposure_times)
hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy(), response=crf_debevec.copy())
cal_robertson = cv.createCalibrateRobertson()
crf_robertson = cal_robertson.process(img_list, times=exposure_times)
hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy(), response=crf_robertson.copy())
