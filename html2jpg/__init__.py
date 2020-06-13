# -*- coding: utf-8 -*-

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# 图片大小
x = 600
y = 280

# 加载背景图
bk_img = cv2.imread("back.png")
# 设置需要显示的字体
fontpath = "msyh.ttc"
# 设置字体大小
font = ImageFont.truetype(fontpath, 23)

# 创建图像
# image转换成array：img = np.asarray(image)
# array转换成image：Image.fromarray(np.uint8(img))
img_pil = Image.fromarray(bk_img)
# 创建新的图像
draw = ImageDraw.Draw(img_pil)
# 绘制文字信息


draw.text((229, 106), "2019-10-10 11:10:10", font=font, fill=(60, 60, 60))
draw.text((229, 189), "10888888888888", font=font, fill=(60, 60, 60))
draw.text((267, 272), "B类", font=font, fill=(60, 60, 60))
draw.text((229, 345), "第一锅", font=font, fill=(60, 60, 60))
draw.text((267, 416), "合格", font=font, fill=(60, 60, 60))
draw.text((267, 475), "合格", font=font, fill=(60, 60, 60))
draw.text((267, 537), "合格", font=font, fill=(60, 60, 60))
draw.text((229, 636), "b", font=font, fill=(60, 60, 60))
draw.text((267, 727), "灭菌物品放行", font=font, fill=(60, 60, 60))
draw.text((229, 799), "小马哥", font=font, fill=(60, 60, 60))
draw.text((229, 882), "高温高压消毒", font=font, fill=(60, 60, 60))
draw.text((229, 987), "纸塑包装类", font=font, fill=(60, 60, 60))
draw.text((229, 1066), "牙科小器械,xxxxxxx,xxxxxx,xxxxx\ndadfjaldjf,daaaa", font=font, fill=(60, 60, 60))

font = ImageFont.truetype(fontpath, 25)
if '物理' == '物理':
    draw.text((48, 1202), "物理检测", font=font, fill=(52, 52, 52))
    draw.text((48, 1592), "化学检测", font=font, fill=(52, 52, 52))
else:
    draw.text((48, 1202), "生物检测", font=font, fill=(52, 52, 52))

# 图片文字生成完毕
# cv2.imshow("add_text", bk_img)
# cv2.waitKey()
bk_img = np.array(img_pil)
cv2.imwrite("file.jpg", bk_img)

if '物理' == '物理':
    # 下载图片并进行图片合成
    img1 = Image.open("test1.jpg")
    img2 = Image.open("test1_1.jpg")
    # x, y = img1.size[0], img1.size[1]
    out1 = img1.resize((x, y), Image.ANTIALIAS)
    out2 = img2.resize((x, y), Image.ANTIALIAS)
    out1.save("test1.jpg")
    out2.save("test1_1.jpg")

    img1 = Image.open("test1.jpg")
    img2 = Image.open("test1_1.jpg")
    bk_img = Image.open("file.jpg")
    bk_img.paste(img1, (48, 1273, 48 + x, 1273 + y))
    bk_img.paste(img2, (48, 1670, 48 + x, 1670 + y))
    bk_img.save("out.jpg")
else:
    # 下载图片并进行图片合成
    img1 = Image.open("test1.jpg")
    # x, y = img1.size[0], img1.size[1]
    out1 = img1.resize((x, y), Image.ANTIALIAS)
    out1.save("test1.jpg")

    img1 = Image.open("test1.jpg")
    bk_img = Image.open("file.jpg")
    bk_img.paste(img1, (48, 1273, 48 + x, 1273 + y))
    bk_img.save("out.jpg")
