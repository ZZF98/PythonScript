from PIL import Image, ImageDraw
from pytesseract import pytesseract

im = Image.open('../download/3.jpg')  # 用pil打开这个图片

im = im.convert('L')
im = im.point(lambda x: 0 if x < 100 else x >= 100, '1')  # 二值化 100为分割灰度的点（阀值），二值化就是将图片的颜色转换成非黑即白的图片
# im = im.point(lambda x: 0 if x < 143 else 255)

# im.show()  # 查看图片


def getPixel(image, x, y):
    L = image.getpixel((x, y))  # 获取当前像素点的像素
    if L == 0:  # 判读此像素点是否为黑，因为如果是白的就没必要处理了
        nearDots = 0  # 初始化记录周围有没有黑像素数量的值
        # 判断周围像素点
        if L - image.getpixel((x - 1, y - 1)):
            nearDots += 1
        if L - image.getpixel((x - 1, y)):
            nearDots += 1
        if L - image.getpixel((x - 1, y + 1)):
            nearDots += 1
        if L - image.getpixel((x, y - 1)):
            nearDots += 1
        if L - image.getpixel((x, y + 1)):
            nearDots += 1
        if L - image.getpixel((x + 1, y - 1)):
            nearDots += 1
        if L - image.getpixel((x + 1, y)):
            nearDots += 1
        if L - image.getpixel((x + 1, y + 1)):
            nearDots += 1
        if nearDots == 8:  # 这里如果周围八个全是白点那么就返回一个白点，实现去黑点的操作
            return 1
        # 这里主要是有俩个黑点连在一起，所有周围会有七个黑点扩大范围进一步判断
        elif nearDots == 7:
            nearDots = 0
            if L - image.getpixel((x - 2, y - 2)):
                nearDots += 1
            if L - image.getpixel((x - 2, y)):
                nearDots += 1
            if L - image.getpixel((x - 2, y + 2)):
                nearDots += 1
            if L - image.getpixel((x, y - 2)):
                nearDots += 1
            if L - image.getpixel((x, y + 2)):
                nearDots += 1
            if L - image.getpixel((x + 2, y - 2)):
                nearDots += 1
            if L - image.getpixel((x + 2, y)):
                nearDots += 1
            if L - image.getpixel((x + 2, y + 2)):
                nearDots += 1
            if nearDots == 8:
                return 1  # 返回白点
            else:
                return 0  # 返回黑点
    else:
        return 1


def clearNoise(image):
    draw = ImageDraw.Draw(image)
    # 循环遍历每个像素点
    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            color = getPixel(image, x, y)
            draw.point((x, y), color)

    return image


# 将上一步处理完成的im对象传给clearNoise()函数
im = clearNoise(im)
# im.save("test.jpg")
# im.show()
result = pytesseract.image_to_string(im, lang='num', config="--psm 7")
print(result)
