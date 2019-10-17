from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


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
    w_pdf = 20 * cm
    h_pdf = 25 * cm

    c = canvas.Canvas(f_pdf, pagesize=(w_pdf, h_pdf))
    c.setFillAlpha(0.5)  # 设置透明度
    # 这里的单位是物理尺寸
    print(c.drawImage(f_jpg, 12 * cm, 17 * cm, 6 * cm, 6 * cm))
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


if __name__ == '__main__':
    f_pdf = "mark.pdf"
    create_watermark('b.jpg', f_pdf)
    add_watermark("a.pdf", f_pdf, "c.pdf")
