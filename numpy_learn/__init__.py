import sys
import matplotlib.pyplot as plt
import numpy as np

a = np.arange(20).reshape(4, 5)
print(a)
# 数组的维度
print('shape', a.shape)
# 数组的轴（维度）的个数
print('ndim', a.ndim)
# 一个描述数组中元素类型的对象
print('dtype', a.dtype.name)
# 数组中每个元素的字节大小
print('itemsize', a.itemsize)
# 数组元素的总数
print('size', a.size)

# 数组创建
a = np.array([2, 3, 4])
b = np.array([(1.5, 2, 3), (4, 5, 6)])
print(a)
print(b)
# 函数zeros创建一个由0组成的数组
a = np.zeros((3, 4))
print(a)
print('-' * 40)
# 函数 ones创建一个完整的数组
a = np.ones((3, 3, 4), dtype=np.int16)
print(a)
# 函数empty 创建一个数组,其初始内容是随机的
a = np.empty((2, 3))
print(a)
print('-' * 40)
# NumPy提供了一个类似于range的函数,该函数返回数组而不是列表
a = np.arange(10, 31, 5)
for num in a:
    print(num)
# 1~5 5步
a = np.linspace(1, 5, 5)
print(a)
print('-' * 40)
b = np.arange(12).reshape(4, 3)  # 2d array
print(b)

c = np.arange(24).reshape(2, 3, 4)
print(c)
print('ndim', c.ndim)
print('-' * 40)
np.set_printoptions(threshold=sys.maxsize)
print(np.arange(10000))
print('-*' * 40)
# 基本操作

a = np.array([20, 30, 40, 50])
b = np.arange(4)
print(a, b)
c = a - b
print(c)
print(b ** 2)
a += b
print(a)
print('-' * 40)
# 通过指定axis 参数,可以沿数组的指定轴应用操作
b = np.arange(12).reshape(3, 4)
print(b)
print(b.sum(axis=1))
print(b.sum(axis=0))
print(b.min(axis=1))
b = np.array([i ** 2 for i in range(5)])
print(b)
print(np.sqrt(b))
# 索引、切片和迭代
print('-*' * 40)
b = np.arange(20).reshape(4, 5)
print(b)
print(b[2, 3])
print(b[0:5, 3])
print(b[:, 3])
print(b[1:3, :])
print(b[-1])

# 改变数组的形状
print('-*' * 40)
for row in b.flat:
    print(row)
print('-' * 40)
# 返回平坦的数组
print(b.ravel())
# 返回形状经过修改的数组
print(b.reshape(10, 2))
# 颠倒数组
print(b.T)
print('-*' * 40)
# 将不同数组堆叠在一起
a = np.floor(10 * np.random.random((2, 2)))
print(a)
b = np.floor(10 * np.random.random((2, 2)))
print(b)
print(np.vstack((a, b)))
print('-' * 40)
print(np.hstack((a, b)))
print('-' * 40)
# 将一个数组拆分成几个较小的数组
a = np.floor(10 * np.random.random((2, 12)))
print(a)
# 沿数组的水平轴拆分数组
for b in np.hsplit(a, 3):
    print(b)
print('-' * 40)
for b in np.vsplit(a, 2):
    print(b)
# 拷贝和视图
# 完全不复制
a = np.arange(12)
b = a
print(b)
# view方法创建一个查看相同数据的新数组对象
c = a.view()
print(c is a)
print(c.base is a)
c.shape = 2, 6
print(c)
print(a.shape)
# 深拷贝
d = a.copy()
print(d is a)
print(d.base is a)
d[0] = 9999
print(d)
print(a)
print('-' * 40)
# 花式索引和索引技巧
a = np.arange(12) ** 2
print(a)
i = np.array([1, 1, 3, 8, 5])
print(a[i])
j = np.array([[3, 4], [9, 7]])
print(a[j])
a = np.arange(5)
a[[1, 3, 4]] = 0
print(a)
print('-' * 40)
# 使用布尔数组进行索引
a = np.arange(12).reshape(3, 4)
b = a > 4
print(b)
print(a[b])
print('-' * 40)
a = np.arange(12).reshape(3, 4)
b1 = np.array([False, True, True])
b2 = np.array([True, False, True, False])
print(a)
print(a[b1, :])
print(a[:, b2])
print(a[b1, b2])
print('-*' * 40)
# 矢量堆叠
x = np.arange(0, 10, 2)
print(x)
y = np.arange(5)
print(y)
m = np.vstack([x, y])
print(m)
xy = np.hstack([x, y])
print(xy)
# 直方图
mu, sigma = 2, 0.5
v = np.random.normal(mu, sigma, 10000)
plt.hist(v, bins=50, density=1)
# plt.show()
(n, bins) = np.histogram(v, bins=50, density=True)
plt.plot(.5 * (bins[1:] + bins[:-1]), n)
plt.show()
