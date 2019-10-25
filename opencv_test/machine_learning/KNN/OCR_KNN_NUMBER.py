import cv2 as cv
import numpy as np

img = cv.imread('digits.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 将图像分割为5000个单元格，每个单元格大小为20x20
cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]
# 把它变成一个Numpy数组。它的大小是(50,100,20,20)
x = np.array(cells)
# 现在我们准备train_data和test_data。
train = x[:, :50].reshape(-1, 400).astype(np.float32)  # Size = (2500,400)
test = x[:, 50:100].reshape(-1, 400).astype(np.float32)  # Size = (2500,400)
# 为培训和测试数据创建标签
k = np.arange(10)
train_labels = np.repeat(k, 250)[:, np.newaxis]
test_labels = train_labels.copy()
# 启动kNN，训练数据，然后使用k=1的测试数据进行测试
knn = cv.ml.KNearest_create()
knn.train(train, cv.ml.ROW_SAMPLE, train_labels)
ret, result, neighbours, dist = knn.findNearest(test, k=5)
# 现在我们检查分类的准确性
# 为此，将结果与test_tags进行比较，并检查哪些是错误的
matches = result == test_labels
correct = np.count_nonzero(matches)
accuracy = correct * 100.0 / result.size
print(accuracy)
# 保存数据
np.savez('knn_data_number.npz', train=train, train_labels=train_labels)
# Now load the data
with np.load('knn_data_number.npz') as data:
    print(data.files)
    train = data['train']
    train_labels = data['train_labels']
