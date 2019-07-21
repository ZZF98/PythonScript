# 识别图片并缓存
from PIL import Image, ImageFilter

kitten = Image.open("download/a.jpg")
blurryKitten = kitten.filter(ImageFilter.GaussianBlur)
blurryKitten.save("cache/a.jpg")
blurryKitten.show()

from PIL import Image
import subprocess

#  图片识别
def cleanFile(filePath, newFilePath):
    image = Image.open(filePath)
    # 对图片进行阈值过滤，然后保存
    image = image.point(lambda x: 0 if x < 143 else 255)
    image.save(newFilePath)
    # 调用系统的tesseract命令对图片进行OCR识别
    subprocess.call(["tesseract", newFilePath, "output"])
    # 打开文件读取结果
    for line in open("output.txt", 'r', encoding='UTF-8'):
        print(line)


cleanFile("download/c.jpg", "text_2_clean.png")
