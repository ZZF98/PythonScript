from __future__ import absolute_import, division, print_function, unicode_literals

# TensorFlow和tf.keras
import tensorflow as tf
from tensorflow import keras

# 助手库
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)
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

print(train_images.shape)
print(len(train_labels))
print(train_labels)