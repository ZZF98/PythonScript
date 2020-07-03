# https://docs.python.org/zh-cn/3/tutorial/
from math import pi


def mye(level):
    if level < 1:
        raise Exception("Invalid level!")
        # 触发异常后，后面的代码就不会再执行


# 测试触发异常
try:
    mye(0)  # 触发异常
except Exception as err:
    print(1, err)
else:
    print(2)


# 函数传参
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])


cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")

s = [str(round(pi, i)) for i in range(1, 60)]
print(s)

matrix = [
    [1, 2, 3, 4, 6],
    [5, 6, 7, 8, 2],
    [9, 10, 11, 12, 1],
    [7, 8, 9, 12, 5], ]
# 行转列
s = [[row[i] for row in matrix] for i in range(5)]
print(s)

# 循环的技巧¶
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)

for i, s in enumerate(['tic', 'tac', 'toe']):
    print(i, " ---- ", str(s))

questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
d_s = ['lancelot_s', 'the holy grail_s', 'blue_s']
for q, a, c in zip(questions, answers, d_s):
    print('What is your {0}?  It is {1}.----{2}'.format(q, a, c))
