# K-Means聚合
"""
使用OpenCV中的cv.kmeans()函数进行数据聚类
samples :它应该属于np。每个特性都应该放在一个单独的列中。
nclusters(K) :最后需要的集群数量
criteria : 它是迭代终止条件。当满足这个条件时，算法停止迭代。实际上，它应该是一个包含3个参数的元组。它们是‘(type, max_iter, epsilon)’:
终止标准的类型。它有3个标志如下:
cv.TERM_CRITERIA_EPS - 如果达到指定的精度，则停止算法迭代。
cv.TERM_CRITERIA_MAX_ITER - 在指定的迭代次数max_iter之后停止算法。
cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER - 当满足上述任何一个条件时，停止迭代。
max_iter - 指定最大迭代次数的整数。
epsilon - 要求精度
attempts : 标记来指定使用不同初始标记执行算法的次数。该算法返回产生最佳密实度的标签。这种紧凑性作为输出返回。
flags : 此标志用于指定如何获取初始中心。通常使用两个标志:cv。KMEANS_PP_CENTERS cv.KMEANS_RANDOM_CENTERS。

Output parameters
compactness : 它是每个点到相应中心距离的平方之和。
labels : 这是label数组(与前一篇文章中的“code”相同)，其中每个元素都标记为“0”、“1”……
centers : 这是集群中心的数组。
"""
# 只有一个特征的数据
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

x = np.random.randint(25, 100, 25)
y = np.random.randint(175, 255, 25)
z = np.hstack((x, y))
z = z.reshape((50, 1))
z = np.float32(z)
plt.hist(z, 256, [0, 256]), plt.show()
# 现在我们应用KMeans函数。在此之前，我们需要指定标准。
# 我的标准是，每当运行10次算法迭代，或者达到epsilon = 1.0的精度时，就停止算法并返回答案。
# 定义条件= (type, max_iter = 10, epsilon = 1.0)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
# 设置标记(只是为了避免代码中的换行)
flags = cv.KMEANS_RANDOM_CENTERS
# 应用KMeans
compactness, labels, centers = cv.kmeans(z, 2, None, criteria, 10, flags)
# 这给了我们紧凑性，标签和中心。在这种情况下，我得到了60个和207个中心。
# 标签的大小将与测试数据的大小相同，每个数据将根据其中心点标记为“0”、“1”、“2”等。
# 现在，我们根据它们的标签将数据分割到不同的集群。
A = z[labels == 0]
B = z[labels == 1]
# 现在我们用红色画出A，用蓝色画出B，用黄色画出它们的中心体。
# Now plot 'A' in red, 'B' in blue, 'centers' in yellow
plt.hist(A, 256, [0, 256], color='r')
plt.hist(B, 256, [0, 256], color='b')
plt.hist(centers, 32, [0, 256], color='y')
plt.show()

# 具有多种特性的数据
X = np.random.randint(25, 50, (25, 2))
Y = np.random.randint(60, 85, (25, 2))
Z = np.vstack((X, Y))
# 转换为np.float32
Z = np.float32(Z)
# 定义标准并应用kmeans()
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret, label, center = cv.kmeans(Z, 2, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
# 现在分离数据，注意flatten()
A = Z[label.ravel() == 0]
B = Z[label.ravel() == 1]
# Plot the data
plt.scatter(A[:, 0], A[:, 1])
plt.scatter(B[:, 0], B[:, 1], c='r')
plt.scatter(center[:, 0], center[:, 1], s=80, c='y', marker='s')
plt.xlabel('Height'), plt.ylabel('Weight')
plt.show()

# 颜色量化
import numpy as np
import cv2 as cv

img = cv.imread('home.jpg')
Z = img.reshape((-1, 3))
# convert to np.float32
Z = np.float32(Z)
# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 2
ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))
cv.imshow('res2', res2)
cv.waitKey(0)
cv.destroyAllWindows()
