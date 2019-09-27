import os

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


# 生成空白文件
def new_image(width, height, color, name):
    img = Image.new('RGB', (width, height), (color["r"], color["g"], color["b"]))
    # img.show()
    img.save(name)


# 创建字体文件
def creat_font_img(value, file_name, path):
    # 编辑图片路径
    img = cv2.imread(path)
    # 设置需要显示的字体
    fontpath = "font/simsun.ttc"
    # 32为字体大小
    font = ImageFont.truetype(fontpath, 32)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    # 获取字体宽度
    sum_width = 0
    sum_height = 0
    for char in value:
        width, height = draw.textsize(char, font)
        sum_width += width
        sum_height = height
    # 绘制文字信息
    # (100,300/350)为字体的位置，(255,255,255)为白色，(0,0,0)为黑色
    draw.text(((img.shape[1] - sum_width) / 2, (img.shape[0] - sum_height) / 2), value, font=font, fill=(0, 0, 0))
    bk_img = np.array(img_pil)
    # cv2.imshow("add_text", bk_img)
    cv2.waitKey()  # 保存图片路径
    cv2.imwrite(file_name + "_font.png", bk_img)


def image_resize(img, size=(1500, 1100)):
    """调整图片大小
    """
    try:
        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')
        img = img.resize(size)
    except Exception as e:
        pass
    return img


# 合并图片（垂直）
def image_merge(images, output_dir='./', output_name='merge.jpg', \
                restriction_max_width=None, restriction_max_height=None):
    """垂直合并多张图片
    images - 要合并的图片路径列表
    ouput_dir - 输出路径
    output_name - 输出文件名
    restriction_max_width - 限制合并后的图片最大宽度，如果超过将等比缩小
    restriction_max_height - 限制合并后的图片最大高度，如果超过将等比缩小
    """
    max_width = 0
    total_height = 0
    # 计算合成后图片的宽度（以最宽的为准）和高度
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            if width > max_width:
                max_width = width
            total_height += height

            # 产生一张空白图
    new_img = Image.new('RGB', (max_width, total_height), 255)
    # 合并
    x = y = 0
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            new_img.paste(img, (x, y))
            y += height

    if restriction_max_width and max_width >= restriction_max_width:
        # 如果宽带超过限制
        # 等比例缩小
        ratio = restriction_max_height / float(max_width)
        max_width = restriction_max_width
        total_height = int(total_height * ratio)
        new_img = image_resize(new_img, size=(max_width, total_height))

    if restriction_max_height and total_height >= restriction_max_height:
        # 如果高度超过限制
        # 等比例缩小
        ratio = restriction_max_height / float(total_height)
        max_width = int(max_width * ratio)
        total_height = restriction_max_height
        new_img = image_resize(new_img, size=(max_width, total_height))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = '%s/%s' % (output_dir, output_name)
    new_img.save(save_path)
    return save_path


color = {}
color["r"] = 255
color["g"] = 255
color["b"] = 255
new_image(430, 100, color, "a.jpg")
creat_font_img("aaaaaaa", "a", "a.jpg")
creat_font_img("好好好", "b", "a.jpg")
creat_font_img("emmmmmmmm", "c", "a.jpg")
image_merge(images=['a_font.png', 'b_font.png', 'c_font.png'], output_name='mer.png')
