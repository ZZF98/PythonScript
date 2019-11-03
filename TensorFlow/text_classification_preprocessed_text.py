# 文本分类与预处理文本
from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
# !pip install -q tensorflow-datasets
import tensorflow_datasets as tfds

tfds.disable_progress_bar()

import numpy as np

# 下载IMDB数据集
print(tf.__version__)
(train_data, test_data), info = tfds.load(
    # 使用预编码了约8k词汇表的版本。
    'imdb_reviews/subwords8k',
    # 以元组的形式返回训练/测试数据集。
    split=(tfds.Split.TRAIN, tfds.Split.TEST),
    # 从数据集(而不是字典)返回(例如，标签)对。
    as_supervised=True,
    # 还返回' info '结构
    with_info=True)

# 尝试编码器
# 数据集信息包括文本编码器(tfd .features.text. subwordtextencoder)。
encoder = info.features['text'].encoder
print('Vocabulary size: {}'.format(encoder.vocab_size))
sample_string = 'Hello TensorFlow.'

encoded_string = encoder.encode(sample_string)
print('Encoded string is {}'.format(encoded_string))

original_string = encoder.decode(encoded_string)
print('The original string: "{}"'.format(original_string))

assert original_string == sample_string
"""
如果字符串不在其字典中，则编码器通过将其分解为子单词或字符来对其进行编码
因此，字符串与数据集越相似，编码后的表示形式就越短
"""
for ts in encoded_string:
    print('{} ----> {}'.format(ts, encoder.decode([ts])))
# 探索数据

for train_example, train_label in train_data.take(1):
    print('Encoded text:', train_example[:10].numpy())
    print('Label:', train_label.numpy())
    print(encoder.decode(train_example))
# 信息结构包含编码器/解码器。编码器可以用来恢复原始文本

# 准备训练资料
"""
您需要为您的模型创建批量的训练数据。评论都是不同的长度
所以使用padded_batch来零填充序列，而批处理
"""
BUFFER_SIZE = 1000

train_batches = (
    train_data
        .shuffle(BUFFER_SIZE)
        .padded_batch(32, train_data.output_shapes))

test_batches = (
    test_data
        .padded_batch(32, train_data.output_shapes))
"""
每个批将有一个形状(batch_size, sequence_length)
因为填充是动态的，每个批将有不同的长度:
"""
for example_batch, label_batch in train_batches.take(2):
    print("Batch shape:", example_batch.shape)
    print("label shape:", label_batch.shape)

# 建模
"""
神经网络是由堆叠层创建的——这需要两个主要的架构决策:
在模型中使用多少层?
每层使用多少隐藏单位?
在本例中，输入数据由一组单词索引组成
要预测的标签不是0就是1。让我们针对这个问题建立一个“连续的单词包”样式模型:
"""
model = keras.Sequential([
    keras.layers.Embedding(encoder.vocab_size, 16),
    keras.layers.GlobalAveragePooling1D(),
    keras.layers.Dense(1, activation='sigmoid')])

model.summary()
# 层依次堆叠，构建分类器:
"""
第一层是嵌入层。这一层使用整数编码的词汇表并查找每个单词索引的嵌入向量
这些向量作为模型火车来学习。这些向量向输出数组添加一个维度
结果维度为:(批量、顺序、嵌入)。

接下来，GlobalAveragePooling1D层通过对序列维数进行平均
为每个示例返回一个固定长度的输出向量
这允许模型以最简单的方式处理可变长度的输入。

这个固定长度的输出向量通过一个具有16个隐藏单元的全连接(密集)层来传输。

最后一层与单个输出节点紧密连接。使用sigmoid激活函数
这个值是0到1之间的一个浮点数，表示一个概率或置信水平。
"""

# 损失函数和优化器
"""
模型需要一个损失函数和一个用于培训的优化器。由于这是一个二进制分类问题
并且模型输出一个概率(一个激活了sigmoid的单单元层)
所以我们将使用binary_crossentropy损失函数。
"""
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 训练模型
"""
通过将数据集对象传递给模型的fit函数来训练模型。设置epoch的数量。
"""
history = model.fit(train_batches,
                    epochs=10,
                    validation_data=test_batches,
                    validation_steps=30)
# 评估模型
"""
让我们看看这个模型是如何运行的。将返回两个值
损失(一个代表我们的错误的数字，越低的值越好)和准确性。
"""
loss, accuracy = model.evaluate(test_batches)

print("Loss: ", loss)
print("Accuracy: ", accuracy)

# 创建一个精确和损失随时间变化的图表
# fit()返回一个历史对象，其中包含一个字典，包含训练期间发生的所有事情:
history_dict = history.history
history_dict.keys()
"""
有四个条目:在培训和验证期间，每个监控指标对应一个条目
我们可以用这些来绘制训练和验证的损失进行比较，以及训练和验证的准确性:
"""
acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)

# "bo" is for "blue dot"
plt.plot(epochs, loss, 'bo', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()
plt.clf()  # clear figure

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')

plt.show()
