# -*-coding:utf-8-*-
# coding:utf-8
import os

# for i in "123456789ABVDEFGHKMNPRSTUVWXYZ":
#     target_path = "fenlei/" + i
#     os.makedirs(target_path)

# for i in "123456789ABCDEFGHKMNPRSTUVWXYZ":
#     part_path = "part/" + i
#     os.makedirs(part_path)

from PIL import Image, ImageDraw

# 二值数组
t2val = {}


def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0


# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image, N, Z):
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1


def saveImage(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])

    image.save(filename)


dir = '../download/'
# 遍历figures下的png,jpg文件
for file in os.listdir(dir):
    if file.endswith('.png') or file.endswith('.jpg'):
        img_path = '%s/%s' % (dir, file)  # 图片路径
        image = Image.open(img_path)

        image = image.convert('L')
        twoValue(image, 198)
        clearNoise(image, 3, 1)
        path1 = "2__erzhihua_jiangzao/" + file + ".jpg"
        saveImage(path1, image.size)

# -*-coding:utf-8-*-


from PIL import Image


def smartSliceImg(img, outDir, ii, count=4, p_w=3):
    '''
    :param img:
    :param outDir:
    :param count: 图片中有多少个图片
    :param p_w: 对切割地方多少像素内进行判断
    :return:
    '''
    w, h = img.size
    pixdata = img.load()
    eachWidth = int(w / count)
    beforeX = 0
    for i in range(count):

        allBCount = []
        nextXOri = (i + 1) * eachWidth

        for x in range(nextXOri - p_w, nextXOri + p_w):
            if x >= w:
                x = w - 1
            if x < 0:
                x = 0
            b_count = 0
            for y in range(h):
                if pixdata[x, y] == 0:
                    b_count += 1
            allBCount.append({'x_pos': x, 'count': b_count})
        sort = sorted(allBCount, key=lambda e: e.get('count'))

        nextX = sort[0]['x_pos']
        box = (beforeX, 0, nextX, h)
        img.crop(box).save(outDir + str(ii) + "_" + str(i) + ".png")
        beforeX = nextX


dir = '../download/'
# 遍历figures下的png,jpg文件
for file in os.listdir(dir):
    if file.endswith('.png') or file.endswith('.jpg'):
        img_path = '%s/%s' % (dir, file)  # 图片路径
        image = Image.open(img_path)
        outDir = '3__qiege/'
        smartSliceImg(image, outDir, file.split(".")[0], count=4, p_w=3)

# -*-coding:utf-8-*-

from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier


def load_dataset():
    X = []
    y = []
    for i in "23456789ABVDEFGHKMNPRSTUVWXYZ":
        target_path = "fenlei/" + i
        print(target_path)
        for title in os.listdir(target_path):
            pix = np.asarray(Image.open(os.path.join(target_path, title)).convert('L'))
            X.append(pix.reshape(25 * 30))
            y.append(target_path.split('/')[-1])

    X = np.asarray(X)
    y = np.asarray(y)
    return X, y


def check_everyone(model):
    pre_list = []
    y_list = []
    for i in "23456789ABCDEFGHKMNPRSTUVWXYZ":
        part_path = "part/" + i
        for title in os.listdir(part_path):
            pix = np.asarray(Image.open(os.path.join(part_path, title)).convert('L'))
            pix = pix.reshape(25 * 30)
            pre_list.append(pix)
            y_list.append(part_path.split('/')[-1])
    pre_list = np.asarray(pre_list)
    y_list = np.asarray(y_list)

    result_list = model.predict(pre_list)
    acc = 0
    for i in result_list == y_list:
        print(result_list, y_list, )

        if i == np.bool(True):
            acc += 1
    print(acc, acc / len(result_list))


X, y = load_dataset()
knn = KNeighborsClassifier()
knn.fit(X, y)
joblib.dump(knn, 'yipai.model')
check_everyone(knn)

# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from sklearn.externals import joblib
import os

target_path = "1__get_image/"
source_result = []
for title in os.listdir(target_path):
    source_result.append(title.replace('.png', ''))


def predict(model):
    predict_result = []
    for q in range(1, 101):
        pre_list = []
        y_list = []
        for i in range(0, 4):
            part_path = "part1/" + str(q) + "_" + str(i) + ".png"
            # print(part_path)
            pix = np.asarray(Image.open(os.path.join(part_path)))
            pix = pix.reshape(25 * 30)
            pre_list.append(pix)
            y_list.append(part_path.split('/')[-1])
        pre_list = np.asarray(pre_list)
        y_list = np.asarray(y_list)

        result_list = model.predict(pre_list)
        print(result_list, q)

        predict_result.append(str(result_list[0] + result_list[1] + result_list[2] + result_list[3]))

    return predict_result


model = joblib.load('yipai.model')
predict_result = predict(model)
# print(source_result)
# print(predict_result)
