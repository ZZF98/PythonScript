from PIL import ImageDraw, Image
from pytesseract import pytesseract


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


im = Image.open('../download/32.jpg')  # 用pil打开这个图片

im = im.convert('L')
# im = im.point(lambda x: 0 if x<50 else 255)
im = im.point(lambda x: 0 if x < 142 else x >= 142, '1')
# im = im.point(lambda x: 0 if x < 143 else 255)
im.show()
# 将上一步处理完成的im对象传给clearNoise()函数
im = clearNoise(im)
im.show()

# lang只用哪个库来识别 默认有个eng库，config 指代识别单行还是多行-psm 7只的是单行
result = pytesseract.image_to_string(im, lang='eng', config="--psm 10")
print(result)
