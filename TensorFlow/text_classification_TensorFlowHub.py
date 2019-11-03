# 文本分类与TensorFlow Hub
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

import tensorflow as tf

# !pip install -q tensorflow-hub
# !pip install -q tensorflow-datasets
import tensorflow_hub as hub
import tensorflow_datasets as tfds

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub version: ", hub.__version__)
print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")

# 下载IMDB数据集
# 将训练集分成60%和40%，我们将得到15000个例子
# 对于培训，10,000个例子用于验证，25,000个例子用于测试。
train_validation_split = tfds.Split.TRAIN.subsplit([6, 4])

(train_data, validation_data), test_data = tfds.load(
    name="imdb_reviews",
    split=(train_validation_split, tfds.Split.TEST),
    as_supervised=True)

# 探索数据
# 标签是0或1的整数值，其中0表示负面评论，1表示正面评论。
# 先打印10个例子
# 再打印前10个标签
train_examples_batch, train_labels_batch = next(iter(train_data.batch(10)))
for data in train_examples_batch:
    print(data)
print(train_labels_batch)

# 建模
# 神经网络是由堆叠层创建的——这需要三个主要的架构决策:
"""
如何表示文本?
在模型中使用多少层?
每层使用多少隐藏单位?
"""
"""
一种表示文本的方法是将句子转换成嵌入向量
我们可以使用一个预先训练好的文本嵌入作为第一层
这将有三个优点:
*我们不必担心文本预处理
*我们可以受益于转移学习
*嵌入有固定的大小，所以处理起来更简单
"""
"""
本例，我们将使用来自TensorFlow Hub的一个预先训练好的文本嵌入模型
名为谷歌/tf2-preview/gnews-swivel-20dim/1
"""
"""
在本教程中，还有其他三个需要测试的预训练模型:
google/tf2-preview/gnews-swivel-20dim-with-oov/1 - 
与谷歌/tf2-preview/gnews-swivel-20dim/1相同，但是将2.5%的词汇表转换为OOV桶
如果任务的词汇表和模型的词汇表没有完全重叠，这将有所帮助
google/tf2-preview/nnlm-en-dim50/1 -
一个大得多的模型~1M词汇量大小和50个维度。
google/tf2-preview/nnlm-en-dim128/1 -
更大的模型，约1M的词汇量和128维。
"""
# 首先创建一个Keras层，它使用TensorFlow Hub模型嵌入句子，并在几个输入示例中进行尝试
# 注意，无论输入文本的长度是多少，embeddings的输出形状都是:(num_examples, embedding_dimension)。
embedding = "https://hub.tensorflow.google.cn/google/tf2-preview/gnews-swivel-20dim/1"
hub_layer = hub.KerasLayer(embedding, input_shape=[],
                           dtype=tf.string, trainable=True)
hub_layer(train_examples_batch[:3])
# 现在让我们建立完整的模型:
model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

model.summary()
"""
1.第一层是TensorFlow Hub层
这一层使用预训练的保存模型将一个句子映射到它的嵌入向量中
我们使用的预先训练好的文本嵌入模型(谷歌/tf2-preview/gnews- swivel20 dim/1)将句子分割成标记
嵌入每个标记，然后结合嵌入。结果的维度是:(num_examples, embedding_dimension)

2.这个固定长度的输出向量通过一个具有16个隐藏单元的全连接(密集)层

3.最后一层与单个输出节点紧密连接
使用sigmoid激活函数，这个值是0到1之间的一个浮点数，表示一个概率或可信度
"""

# 损失函数和优化器
"""
模型需要一个损失函数和一个用于培训的优化器。
由于这是一个二进制分类问题，并且模型输出一个概率(一个激活了sigmoid的单单元层)
所以我们将使用binary_crossentropy损失函数

这不是损失函数的惟一选择
例如，可以选择mean_squared_error
但是，一般来说，binary_crossentropy更适合处理概率—它测量概率分布之间的“距离”
或者在我们的例子中，测量地面真实分布和预测之间的“距离”
"""
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 训练模型
"""
以512个样品小批量培养20个epoch的模型
这是x_train和y_train张量中所有样本的20次迭代
在训练过程中，对来自验证集的10,000个样本监测模型的损失和准确性:
"""
history = model.fit(train_data.shuffle(10000).batch(512),
                    epochs=20,
                    validation_data=validation_data.batch(512),
                    verbose=1)

# 评估模型
results = model.evaluate(test_data.batch(512), verbose=2)

for name, value in zip(model.metrics_names, results):
    print("%s: %.3f" % (name, value))
# 这种相当天真的方法获得了大约87%的准确性。使用更高级的方法，模型应该接近95%。

