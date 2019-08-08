# 识别验证码
# -*-coding:utf-8-*-
import os


def test(path):
    img = Image.open(path)
    w, h = img.size
    for x in range(w):
        for y in range(h):
            r, g, b = img.getpixel((x, y))
            if 190 <= r <= 255 and 170 <= g <= 255 and 0 <= b <= 140:
                img.putpixel((x, y), (0, 0, 0))
            if 0 <= r <= 90 and 210 <= g <= 255 and 0 <= b <= 90:
                img.putpixel((x, y), (0, 0, 0))
    img = img.convert('L').point([0] * 150 + [1] * (256 - 150), '1')
    return img


# -*-coding:utf-8-*-


# coding:utf-8
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


# -*-coding:utf-8-*-

from PIL import Image
import pytesseract


def recognize_captcha(img_path):
    im = Image.open(img_path)
    # threshold = 140
    # table = []
    # for i in range(256):
    #     if i < threshold:
    #         table.append(0)
    #     else:
    #         table.append(1)
    #
    # out = im.point(table, '1')
    num = pytesseract.image_to_string(im)
    return num


if __name__ == '__main__':
    dir = '../download/'
    # dir = './image/'
    # dir = './'

    correct_count = 0  # 图片总数
    total_count = 0  # 识别正确的图片数量

    # 遍历figures下的png,jpg文件
    for file in os.listdir(dir):
        if file.endswith('.png') or file.endswith('.jpg'):
            img_path = '%s/%s' % (dir, file)  # 图片路径
            res = recognize_captcha(img_path)
            strs = res.split("\n")
            if len(strs) >= 1:
                print(file + ":" + strs[0])
