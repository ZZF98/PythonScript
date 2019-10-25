import cv2 as cv
import numpy as np

# 加载数据后，转换器将字母转换成数字
data = np.loadtxt('letter-recognition.data', dtype='float32', delimiter=',',
                  converters={0: lambda ch: ord(ch) - ord('A')})
# 将数据分成两份，10000份用于培训和测试
train, test = np.vsplit(data, 2)
# 将trainData和testData分解为特性和响应
responses, trainData = np.hsplit(train, [1])
labels, testData = np.hsplit(test, [1])
# 启动kNN，分类，测量精度
knn = cv.ml.KNearest_create()
knn.train(trainData, cv.ml.ROW_SAMPLE, responses)
ret, result, neighbours, dist = knn.findNearest(testData, k=5)
correct = np.count_nonzero(result == labels)
accuracy = correct * 100.0 / 10000
print(accuracy)

np.savez('knn_data_english.npz', train=train, train_labels=responses)
# Now load the data
with np.load('knn_data_english.npz') as data:
    print(data.files)
    train = data['train']
    train_labels = data['train_labels']
    print(train)
    print(train_labels)
