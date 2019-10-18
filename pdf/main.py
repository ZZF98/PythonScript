import os

from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


# pip3 install pdf2image
# https://github.com/Belval/pdf2image

# 创建文字pdf
def create_watermark(content):
    # 默认大小为21cm*29.7cm
    c = canvas.Canvas("mark.pdf", pagesize=(30 * cm, 30 * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(10 * cm, 5 * cm)

    # 设置字体
    c.setFont("Helvetica", 80)
    # 指定描边的颜色
    c.setStrokeColorRGB(0, 1, 0)
    # 指定填充颜色
    c.setFillColorRGB(0, 1, 0)
    # 画一个矩形
    c.rect(cm, cm, 7 * cm, 17 * cm, fill=1)
    # 旋转45度，坐标系被旋转
    c.rotate(45)
    # 指定填充颜色
    c.setFillColorRGB(0.6, 0, 0)
    # 设置透明度，1为不透明
    c.setFillAlpha(0.3)
    # 画几个文本，注意坐标系旋转的影响
    c.drawString(3 * cm, 0 * cm, content)
    c.setFillAlpha(0.6)
    c.drawString(6 * cm, 3 * cm, content)
    c.setFillAlpha(1)
    c.drawString(9 * cm, 6 * cm, content)

    # 关闭并保存pdf文件
    c.save()


# create_watermark('walker')


# 制作图片水印pdf
def create_watermark(f_jpg, f_pdf):
    w_pdf = 25 * cm
    h_pdf = 30 * cm

    c = canvas.Canvas(f_pdf, pagesize=(w_pdf, h_pdf))
    c.setFillAlpha(0.5)  # 设置透明度
    # 这里的单位是物理尺寸
    print(c.drawImage(f_jpg, 15.4 * cm, 23 * cm, 6 * cm, 6 * cm))
    c.save()


# 所有路径为绝对路径
def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    pdf_output = PdfFileWriter()
    pdf_input = PdfFileReader(open(pdf_file_in, 'rb'))
    # PDF文件被加密了
    if pdf_input.getIsEncrypted():
        print('该PDF文件被加密了.')
        # 尝试用空密码解密
        try:
            pdf_input.decrypt('')
        except Exception as e:
            print('尝试用空密码解密失败.')
            return False
        else:
            print('用空密码解密成功.')

    # 获取PDF文件的页数
    pageNum = pdf_input.getNumPages()
    # 读入水印pdf文件
    pdf_watermark = PdfFileReader(open(pdf_file_mark, 'rb'))
    # 给每一页打水印
    for i in range(pageNum):
        page = pdf_input.getPage(i)
        page.mergePage(pdf_watermark.getPage(0))
        page.compressContentStreams()  # 压缩内容
        pdf_output.addPage(page)
        print("第{}页".format(i))

    with open(pdf_file_out, 'wb') as out:
        pdf_output.write(out)


# pdf转png
def pdf_pic(fn):
    pages = convert_from_path(fn)
    file_name = fn.split('.')[0]
    for i in range(0, len(pages)):
        new_name = file_name + str((i + 1))
        pages[i].save(f"" + new_name + ".png", 'PNG')
        print("生成图片：{}".format(new_name))


def pic_add_watermark(fn, watermark):
    file_name = fn.split('.')[0]
    list = os.listdir(os.getcwd())
    i = 0
    file_list = []
    # 寻找文件列表
    for file in list:
        if file_name in file and file.endswith(".png"):
            print(file)
            file_list.append(file)
            i = i + 1
    print(file_list)
    print(i)
    # 图片合成
    for file in file_list:
        background = Image.open(file)
        foreground = Image.open(watermark)
        background.paste(foreground, (background.size[0] - foreground.size[0], 20), foreground)
        background.save(file)

    im_list = []
    for each_image in range(i):
        try:
            img = Image.open(file_name + str((each_image + 2)) + ".png")
        except:
            continue
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    new_pdf = file_name + "_watermark.pdf"
    if not os.path.isfile(file_name + "_watermark.pdf"):  # 无文件时创建
        fd = open(new_pdf, mode="w", encoding="utf-8")
        fd.close()
    pdf = Image.open(file_list[0])
    pdf.save(new_pdf, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    for file in file_list:
        os.remove(file)


# 图片覆盖
def test():
    background = Image.open("曾炜口腔诊所-服务报告书首页4.png")
    foreground = Image.open("a.jpg")
    background.paste(foreground, (0, 0), foreground)
    background.show()


if __name__ == '__main__':
    pdf_pic("曾炜口腔诊所-服务报告书首页.pdf")
    pic_add_watermark("曾炜口腔诊所-服务报告书首页.pdf", "a.jpg")
# f_pdf = "mark.pdf"
# create_watermark('a.jpg', f_pdf)
# add_watermark("曾炜口腔诊所-服务报告书首页.pdf", f_pdf, "c.pdf")
