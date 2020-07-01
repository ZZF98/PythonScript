import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# pandas有两种数据结构
# Series
s = pd.Series([1, 2, 3, np.nan, 5, 6])
print(s)
s = pd.Series([1, 2, 3, np.nan, 5, 6], [1, 2, 3, 4, 5, 6])
print(s)
print("----------------------------------------------------------------------\n")

# DataFrame
# DataFrame是表格型数据结构,包含一组有序的列,每列可以是不同的值类型.
# DataFrame有行索引和列索引,可以看成由Series组成的字典.
# 用含日期时间索引与标签的 NumPy 数组生成 DataFrame
dates = pd.date_range('20200701', periods=6)
pd1 = pd.DataFrame(np.random.randn(6, 5), index=dates, columns=['A', 'B', 'C', 'D', 'E'])

print('输出6行5列的表格：')
print(pd1, '\n')

print('输出第E列：')
print(pd1['E'], '\n')

print('切片选择：')
print(pd1[0:3], '\n', pd1['20200701':'20200704'], '\n')

print('根据行标签进行选择数据：')
print(pd1.loc['20200701', ['A', 'B']], '\n')

print('输出第3行第2列的数据：')
print(pd1.iloc[2, 1], '\n')

print('进行切片选择：')
print(pd1.iloc[3:5, 0:2], '\n')

print('进行不连续筛选：')
print(pd1.iloc[[1, 2, 4], [0, 1, 2]], '\n')

print('根据判断筛选：')
print(pd1[pd1.B > 0], '\n')

print('输出20200703行E列的数据（并更新为999）：')
print(pd1.loc['20200703', ['E']], '\n')
pd1.loc['20200703', ['E']] = 999
print(pd1, '\n')

print('根据条件设置值：')
pd1[pd1.B > 0] = 888
print(pd1, '\n')

print('根据列设置：', '\n')
pd1['C'] = np.nan
print(pd1, '\n')
print('根据行设置：', '\n')
pd1[3:4] = np.nan
print(pd1, '\n')
print('根据索引设置：', '\n')
pd1.loc['20200701', ['A', 'E']] = np.nan
print(pd1, '\n')
print("----------------------------------------------------------------------\n")
print('通过字典创建DataFrame：')
df_1 = pd.DataFrame({'A': 1.0,
                     # 'B': pd.Timestamp(2020, 7, 1),
                     'B': pd.date_range('20200701', periods=5),
                     'C': pd.Series(1, index=list(range(5)), dtype='float32'),
                     'D': np.array([9] * 5, dtype='int32'),
                     'E': pd.Categorical(['test1', 'test2', 'test3', 'test4', 'test5']),
                     'F': 'ALL',
                     'G': [1, 2, 3, 4, 5]})
print(df_1, '\n')

print('返回每列的数据类型：')
print(df_1.dtypes, '\n')

print('返回行的序号：')
print(df_1.index, '\n')

print('返回列的序号名字：')
print(df_1.columns, '\n')

print('把每个值进行打印出来：')
print(df_1.values, '\n')

print('数字总结：')
print(df_1.describe(), '\n')

print('翻转数据：')
print(df_1.T, '\n')

print('按轴排序：')
# axis等于1按列进行排序 如ABCDEFG 然后ascending倒叙进行显示
print(df_1.sort_index(1, ascending=False), '\n')

print('按值排序：')
print(df_1.sort_values('G'), '\n')

print('输出第E列：')
print(df_1['E'], '\n')

print('切片选择：')
print(df_1[1:4], '\n')

print('根据判断筛选：')
print(df_1[df_1.G > 2], '\n')

print('输出第3行第7列的数据：')
print(df_1.iloc[2, 6], '\n')
df_1.iloc[2, 6] = 999
print('修改后', df_1.iloc[2, 6], '\n')

print('添加数据：')
df_1['H'] = pd.Series([0, 1, None, 3, 4])
df_1['I'] = pd.Series([1, 2, 3], index=[0, 2, 4])
print(df_1, '\n')
print("----------------------------------------------------------------------\n")
# Pandas处理丢失数据
dates = pd.date_range('2020-07-01', periods=6)
df = pd.DataFrame(np.arange(30).reshape(6, 5), index=dates, columns=['A', 'B', 'C', 'D', 'E'])
df.iloc[0, 1] = np.nan
df.iloc[1, 2] = np.nan

print('输出6行5列的数据：')
print(df, '\n')

print('使用dropna()函数去掉NaN的行或列：')
# 0对行进行操作 1对列进行操作 any:只要存在NaN即可drop掉 all:必须全部是NaN才可drop

print(df.dropna(0, how='any'), '\n')
print('使用fillna()函数替换NaN值：')

# 将NaN值替换为0
print(df.fillna(value=0), '\n')

print('使用isnull()函数判断数据是否丢失：')
print(pd.isnull(df), '\n')

# Pandas导入导出
print('将资料存储成csv文件：')
df.to_csv('test.csv')

print('读取csv文件：')
csv_data = pd.read_csv('test.csv')
print(csv_data, '\n')

print("----------------------------------------------------------------------\n")
# Pandas合并数据
df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['a', 'b', 'c', 'd'])
df3 = pd.DataFrame(np.ones((3, 4)) * 2, columns=['a', 'b', 'c', 'd'])

# 0表示竖项合并 1表示横项合并 ingnore_index重置序列index index变为0 1 2 3 4 5 6 7 8
res = pd.concat([df1, df2, df3], axis=0, ignore_index=True)
print('竖项合并\n', res, '\n')

res = pd.concat([df1, df2, df3], axis=1, ignore_index=True)
print('横项合并\n', res, '\n')

# join合并方式
df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'], index=[1, 2, 3])
df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['a', 'b', 'c', 'd'], index=[2, 3, 4])
print('第一个数据为：')
print(df1, '\n')
print('第二个数据为：')
print(df2, '\n')

print('join行往外合并:相当于全连接')
res = pd.concat([df1, df2], axis=1, join='outer')
print(res, '\n')

print('join行相同的进行合并:相当于内连接')
res2 = pd.concat([df1, df2], axis=1, join='inner')
print(res2, '\n')
print("----------------------------------------------------------------------\n")

# append添加数据
df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['a', 'b', 'c', 'd'])
df3 = pd.DataFrame(np.ones((3, 4)) * 2, columns=['a', 'b', 'c', 'd'])
s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
s2 = pd.Series([2, 4, 6, 8], index=['a', 'b', 'c', 'd'])

print('将df2合并到df1的下面 并重置index')
res = df1.append(df2, ignore_index=True)
print(res, '\n')

print('将s1合并到df1的下面，并重置index')
res2 = df1.append(s1, ignore_index=True)
res2 = res2.append(s2, ignore_index=True)
print(res2, '\n')

print("----------------------------------------------------------------------\n")
# Pandas合并merge
# 依据一组key合并
left = pd.DataFrame({'key': ['k0', 'k1', 'k2', 'k3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
print('第一个数据为：')
print(left, '\n')

right = pd.DataFrame({'key': ['k2', 'k3', 'k4', 'k5'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print('第二个数据为：')
print(right, '\n')

print('依据key进行merge:')
res = pd.merge(left, right, on='key')
print(res, '\n')

right = pd.DataFrame({'key': ['k0', 'k1', 'k2', 'k3'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print('依据key进行merge:')
res = pd.merge(left, right, on='key')
print(res, '\n')
print("----------------------------------------------------------------------\n")
# 依据两组key合并
left = pd.DataFrame({'key1': ['k0', 'k1', 'k2', 'k3'],
                     'key2': ['k0', 'k1', 'k0', 'k1'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
print('第一个数据为：')
print(left, '\n')

right = pd.DataFrame({'key1': ['k0', 'k1', 'k2', 'k3'],
                      'key2': ['k0', 'k0', 'k0', 'k0'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print('第二个数据为：')
print(right, '\n')

print('内联合并')
res = pd.merge(left, right, on=['key1', 'key2'], how='inner')
print(res, '\n')

print('外联合并')
res2 = pd.merge(left, right, on=['key1', 'key2'], how='outer')
print(res2, '\n')

print('左联合并')
res3 = pd.merge(left, right, on=['key1', 'key2'], how='left')
print(res3, '\n')

print('右联合并')
res4 = pd.merge(left, right, on=['key1', 'key2'], how='right')
print(res4, '\n')
print("----------------------------------------------------------------------\n")
# Indicator合并
df1 = pd.DataFrame({'col1': [0, 1], 'col_left': ['a', 'b']})
df2 = pd.DataFrame({'col1': [1, 2, 2], 'col_right': [2, 2, 2]})
print('第一个数据为：')
print(df1, '\n')

print('第二个数据为：')
print(df2, '\n')

print('依据col1进行合并 并启用indicator=True输出每项合并方式:')
res = pd.merge(df1, df2, on='col1', how='outer', indicator=True)
print(res, '\n')
print("----------------------------------------------------------------------\n")
# 依据index合并
left = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2']},
                    index=['k0', 'k1', 'k2'])

right = pd.DataFrame({'C': ['C0', 'C1', 'C2'],
                      'D': ['D0', 'D1', 'D2']},
                     index=['k0', 'k2', 'k3']
                     )

print('第一个数据为：')
print(left, '\n')

print('第二个数据为：')
print(right, '\n')

print('根据index索引进行合并 并选择外联合并')
res = pd.merge(left, right, left_index=True, right_index=True, how='outer')
print(res, '\n')

print('根据index索引进行合并 并选择内联合并')
res2 = pd.merge(left, right, left_index=True, right_index=True, how='inner')
print(res2, '\n')
# 字符串方法
s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
print(s.str.lower())
print("----------------------------------------------------------------------\n")
# 可视化
df = pd.DataFrame(np.random.randn(1000, 4), columns=['A', 'B', 'C', 'D'])
df = df.cumsum()
# plt.figure()
df.plot()
plt.legend(loc='best')
plt.show()
