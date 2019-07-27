# 识别图片并缓存
# from PIL import Image, ImageFilter
#
# kitten = Image.open("download/a.jpg")
# blurryKitten = kitten.filter(ImageFilter.GaussianBlur)
# blurryKitten.save("cache/a.jpg")
# blurryKitten.show()

from PIL import Image
import subprocess

import pyocr
import pyocr.builders

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


cleanFile("download/3.jpg", "cache/cache.jpg")
# subprocess.call(["tesseract", "./out_img/test-interferencePoint.jpg", "../output"])
# # 打开文件读取结果
# for line in open("../output.txt", 'r', encoding='UTF-8'):
#     print(line)
# test
# import time
# from urllib.request import urlretrieve
# import subprocess
# from selenium import webdriver
#
# # 创建新的Selenium driver
# driver = webdriver.PhantomJS(executable_path='download/phantomjs.exe')
# # 有时我发现PhantomJS查找元素有问题,但是Firefox没有。
# # 如果你运行程序的时候出现问题，去掉下面这行注释，
# # 用Selenium试试Firefox浏览器：
# # driver = webdriver.Firefox()
# driver.get(
#     "http://www.amazon.com/War-Peace-Leo-Nikolayevich-Tolstoy/dp/1427030200")
# time.sleep(2)
# # 单击图书预览按钮
# driver.find_element_by_id("sitbLogoImg").click()
# imageList = set()
# # 等待页面加载完成
# time.sleep(5)
# # 当向右箭头可以点击时，开始翻页
# while "pointer" in driver.find_element_by_id("sitbReaderRightPageTurner").get_attribute("style"):
#     driver.find_element_by_id("sitbReaderRightPageTurner").click()
#     time.sleep(2)
#     # 获取已加载的新页面（一次可以加载多个页面，但是重复的页面不能加载到集合中）
#     pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")
#     for page in pages:
#         image = page.get_attribute("src")
#     imageList.add(image)
# driver.quit()
# # 用Tesseract处理我们收集的图片URL链接
# for image in sorted(imageList):
#     urlretrieve(image, "page.jpg")
#     p = subprocess.Popen(["tesseract", "page.jpg", "page"],
#                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     p.wait()
#     f = open("page.txt", "r")
#     print(f.read())
