import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# 包含25个已知/训练数据的(x,y)值的特征集
trainData = np.random.randint(0, 100, (40, 3)).astype(np.float32)
# 用数字0和1分别标记红色或蓝色，2为绿色
responses = np.random.randint(0, 3, (40, 1)).astype(np.float32)
# 把红色家庭画出来
red = trainData[responses.ravel() == 0]
plt.scatter(red[:, 0], red[:, 1], 80, 'r', '^')
# 把蓝色的家庭画出来
blue = trainData[responses.ravel() == 1]
plt.scatter(blue[:, 0], blue[:, 1], 80, 'b', 's')
# 把绿的家庭画出来
green = trainData[responses.ravel() == 2]
plt.scatter(green[:, 0], green[:, 1], 80, 'g', 'x')
# plt.show()

# 给新来者的标签是根据我们前面看到的kNN理论。如果你想要最近邻算法，只需指定k=1，其中k是近邻的数量。
# k近邻的标签。
# 从新来者到每个最近邻居的相应距离。
newcomer = np.random.randint(0, 100, (1, 3)).astype(np.float32)
plt.scatter(newcomer[:, 0], newcomer[:, 1], 80, 'y', 'o')
knn = cv.ml.KNearest_create()
knn.train(trainData, cv.ml.ROW_SAMPLE, responses)
ret, results, neighbours, dist = knn.findNearest(newcomer, 5)
print("结果:  {}\n".format(results))
print("邻居节点:  {}\n".format(neighbours))
print("距离:  {}\n".format(dist))
plt.show()
