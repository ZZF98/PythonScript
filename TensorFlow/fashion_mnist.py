# 对服装图像进行分类
from __future__ import absolute_import, division, print_function, unicode_literals

# 助手库
import matplotlib.pyplot as plt
import numpy as np
# TensorFlow和tf.keras
import tensorflow as tf
from tensorflow import keras

print(tf.__version__)


def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array, true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         class_names[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array, true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


# 加载数据
"""
加载数据集返回四个NumPy数组:
train_images和train_label数组是训练集——模型用来学习的数据。
模型将根据测试集test_images和test_label数组进行测试。
"""
fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

"""
每个图像都映射到单个标签。由于类名没有包含在数据集中，所以将它们存储在这里，以便以后绘制图像时使用:
"""
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# 训练集
print(train_images.shape)
print(len(train_labels))
print(train_labels)
# 测试集
print(test_images.shape)
print(len(test_images))
# 在训练网络之前，必须对数据进行预处理
# 如果你检查训练集中的第一个图像，你会看到像素值落在0到255的范围内:
plt.figure()
a = train_images[0]
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

"""
将这些值缩放到0到1的范围
为此，将这些值除以255。重要的是，训练集和测试集以相同的方式预处理
"""
train_images = train_images / 255.0

test_images = test_images / 255.0
"""
为了验证数据的格式是否正确
以及您是否准备好构建和训练网络
让我们显示来自训练集的前25个图像
并在每个图像下面显示类名
"""
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

# 建模
# 设置图层
"""
神经网络的基本构件是层
层从输入的数据中提取表示
大多数深度学习是由简单的层次链接在一起构成的
比如tf.keras.layers
"""
"""
这个网络的第一层，tf.keras.layers.Flatten
将图像的格式从一个二维数组(28×28像素)转换为一个一维数组(28 * 28 = 784像素)
可以把这个层看作是将图像中的像素行分解并排列起来
这一层没有需要学习的参数;它只重新格式化数据
当像素被压平后，网络由两个tf.keras.layers.Dense组成的序列组成层
这些神经层紧密相连第一Dense层有128个节点(或神经元)
第二层(也是最后一层)是一个10节点的softmax层，它返回一个10个概率值的数组，这些概率值的和为1
每个节点包含一个分数，表示当前图像属于10个类之一的概率
"""
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# 编译模型
"""
在模型准备好进行培训之前它需要更多的设置
这些是在模型的编译步骤中添加的:
"""
"""
Optimizer     ——这是根据它看到的数据和它的损失函数更新模型的方法
loss function ——测量训练过程中模型的准确性,您想要最小化这个函数来“引导”模型朝正确的方向前进
metrics       ——用于监视培训和测试步骤,下面的例子使用精度,即正确分类的图像的分数
"""
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 训练模型
"""
训练神经网络模型需要以下步骤:
"""
"""
1.将训练数据输入模型,在本例中,训练数据位于train_images和train_tags数组中
2.这个模型学会了把图像和标签联系起来
3.您要求模型对一个测试集做出预测—在这个例子中:test_images数组,验证预测是否与test_labels数组中的标签匹配
"""
# 要开始训练，使用model.fit 方法——之所以这么叫，是因为它将模型“适合”于训练数据:
# 当模型训练时，显示损失和精度指标。该模型对训练数据的准确率约为0.9099(或90%)
model.fit(train_images, train_labels, epochs=10)

# 评估准确性
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
# 结果表明，测试数据集的准确性略低于训练数据集的准确性
# 这种训练精度和测试精度之间的差距表示过度拟合
# 过度拟合是指机器学习模型在新的、以前未见过的输入上的表现不如在训练数据上的表现
print('\nTest accuracy:', test_acc)

# 作出预测
# 通过训练模型，您可以使用它对一些图像进行预测
predictions = model.predict(test_images)
# 模型已经预测了测试集中每张图片的标签
# 让我们看一下第一个预测
print(predictions[0])
print(class_names[int(np.argmax(predictions[0]))])

# 绘制这张图来查看完整的10个类预测
"""
让我们看看第0张图片、预测和预测数组
正确的预测标签是蓝色的，错误的预测标签是红色的
这个数字给出了预测标签的百分比(满分100)
"""
for i in range(3):
    plt.figure(figsize=(6, 3))
    plt.subplot(1, 2, 1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(1, 2, 2)
    plot_value_array(i, predictions[i], test_labels)
    plt.show()

# 绘制错误情况
num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
    plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()

# 最后
# 利用训练后的模型对单个图像进行预测
img = test_images[1]
print(img.shape)
"""
tf.keras模型经过优化
可以一次对一批或一组示例进行预测
因此,即使你使用的是一张图片,你也需要将它添加到一个列表中:
"""
# 将图像添加到批处理中，其中它是唯一的成员。
img = (np.expand_dims(img, 0))
print(img.shape)
# 现在预测这个图像的正确标签:
predictions_single = model.predict(img)

print(predictions_single)
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
# 绘图
plot_image(1, predictions_single[0], test_labels, test_images)
plt.subplot(1, 2, 2)
# 绘制列表
plot_value_array(1, predictions_single[0], test_labels)
_ = plt.xticks(range(10), class_names, rotation=90)
plt.show()
"""
model.predict 返回一个列表列表-为批处理数据中的每个图像一个列表。抓住预测我们的(唯一的)图像批:
"""
print(class_names[int(np.argmax(predictions_single[0]))])
