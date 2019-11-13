# -*- coding:utf-8 -*-
# 消费者
import base64
import json
import os
import smtplib
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pika
import requests
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path

# 登陆
loginData = {"username": "XXXXXXXXXXXX", "password": "XXXXXXXXXXXXXXXXXXXXXX"}
address = 'XXXXXXXXXXXXXXXX:8999'

# 连接
# auth info
auth = pika.PlainCredentials('guest', 'guest')  # auth info
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1', 5672, '/', auth))  # connect to rabbit
channel = connection.channel()  # create channel

# 申明队列
channel.queue_declare(queue='PDF-WATERMARK', durable=True, passive=True)


# 发送短信
class SendMail(object):
    def __init__(self, username, passwd, recv, title, content,
                 file=None, ssl=False,
                 email_host='smtp.qq.com', port=25, ssl_port=465):
        '''
        :param username: 用户名
        :param passwd: 密码
        :param recv: 收件人，多个要传list ['a@qq.com','b@qq.com]
        :param title: 邮件标题
        :param content: 邮件正文
        :param file: 附件路径，如果不在当前目录下，要写绝对路径，默认没有附件
        :param ssl: 是否安全链接，默认为普通
        :param email_host: smtp服务器地址，默认为163服务器
        :param port: 非安全链接端口，默认为25
        :param ssl_port: 安全链接端口，默认为465
        '''
        self.username = username  # 用户名
        self.passwd = passwd  # 密码
        self.recv = recv  # 收件人，多个要传list ['a@qq.com','b@qq.com]
        self.title = title  # 邮件标题
        self.content = content  # 邮件正文
        self.file = file  # 附件路径，如果不在当前目录下，要写绝对路径
        self.email_host = email_host  # smtp服务器地址
        self.port = port  # 普通端口
        self.ssl = ssl  # 是否安全链接
        self.ssl_port = ssl_port  # 安全链接端口

    def send_mail(self):
        msg = MIMEMultipart()
        # 发送内容的对象
        if self.file:  # 处理附件的
            file_name = os.path.split(self.file)[-1]  # 只取文件名，不取路径
            try:
                f = open(self.file, 'rb').read()
            except Exception as e:
                raise Exception('附件打不开！！！！')
            else:
                att = MIMEText(f, "base64", "utf-8")
                att["Content-Type"] = 'application/octet-stream'
                # base64.b64encode(file_name.encode()).decode()
                new_file_name = '=?utf-8?b?' + base64.b64encode(file_name.encode()).decode() + '?='
                # 这里是处理文件名为中文名的，必须这么写
                att["Content-Disposition"] = 'attachment; filename="%s"' % (new_file_name)
                msg.attach(att)
        msg.attach(MIMEText(self.content))  # 邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.username  # 发送者账号
        msg['To'] = ','.join(self.recv)  # 接收者账号列表
        if self.ssl:
            self.smtp = smtplib.SMTP_SSL(self.email_host, port=self.ssl_port)
        else:
            self.smtp = smtplib.SMTP(self.email_host, port=self.port)
        # 发送邮件服务器的对象
        self.smtp.login(self.username, self.passwd)
        try:
            self.smtp.sendmail(self.username, self.recv, msg.as_string())
            pass
        except Exception as e:
            print('发送失败', e)
        else:
            print('发送成功！')
        self.smtp.quit()


# pdf转png
def pdf_pic(fn):
    pages = convert_from_path(fn)
    file_name = fn.split('.')[0]
    for i in range(0, len(pages)):
        new_name = file_name + str((i + 1))
        pages[i].save("" + new_name + ".png", 'PNG')
        print("生成图片：{}".format(new_name))


# 图片添加水印
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
    file_list.sort()
    # 图片合成
    for file in file_list:
        background = Image.open(file)
        foreground = Image.open(watermark)
        background.paste(foreground, (background.size[0] - foreground.size[0] - 200, 150), foreground)
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
    # 保存pdf
    pdf.save(new_pdf, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    # 删除图片
    for file in file_list:
        os.remove(file)
    return new_pdf


# 所有路径为绝对路径
def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    pdf_output = PdfFileWriter()
    input = open(pdf_file_in, 'rb')
    pdf_input = PdfFileReader(input)
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
    input.close()


# 获取admin token
def getAdminToken():
    r = requests.post("http://{}/api/v2/unsecure/login".format(address), json=loginData)
    token = json.loads(r.text)['data']['token']
    return token


def uploadPDF(id, headers, new_name, order_url):
    # 重试三次
    for i in range(3):
        try:
            files = {"file": open(new_name, "rb")}
            # 超时时间为3分钟
            url = "http://{}/api/v2/secure/customer/department/{}/file".format(address, id)
            data = {"type": "MANUAL", "name": id, "oldFile": order_url}
            r = requests.post(url, headers=headers, files=files, data=data)
            if r.status_code == 200:
                if r.json()['data'] == True:
                    print("upload video:" + r.text)
                    return True
                else:
                    print("失败")
            else:
                print("upload video yes:" + r.text)
                continue
        except Exception as e:
            # print("erro")
            print(e)
            pass
    return False


# 回调
def callback(ch, method, properties, body):
    # 获取token
    token = getAdminToken()
    print(token)
    # 解析json
    jsons = json.loads(str(body.decode()))
    try:
        print(jsons)
        # 重试三次
        for i in range(3):
            # 下载pdf
            try:
                urllib.request.urlretrieve(jsons["url"], str(jsons["url"]).split("/")[-1])
                break
            except:
                pass

        list = os.listdir(os.getcwd())
        for file in list:
            if file != 'mark.pdf' and file.endswith(".pdf"):
                # 打水印生成pdf
                file_name = file
                print(file)
                pdf_pic(file_name)
                new_pdf = pic_add_watermark(file_name, "a.png")
                # 添加文字水印
                f_pdf = 'mark.pdf'
                add_watermark(new_pdf, f_pdf, file_name)
                os.remove(new_pdf)
                headers = {"X-Authorization": "Bearer " + token}
                data = uploadPDF(jsons["departmentId"], headers, file_name, jsons["url"])
                if data:
                    os.remove(file_name)
                else:
                    m = SendMail(
                        username='XCCCCCCCCCCCC@QQ.com',
                        passwd='XCXXXXXXXX',
                        recv=['XXXXXXXX@QQ.com'],
                        title='PDF打水印失败',
                        content='文件信息:' + str(jsons) + "\n请手动上传",
                        file=r"{" + file_name + "}",
                        ssl=True,
                    )
                    m.send_mail()
    except:
        m = SendMail(
            username='XCCCCCCCCCCCC@QQ.com',
            passwd='XCXXXXXXXX',
            recv=['XXXXXXXX@QQ.com'],
            title='PDF打水印失败',
            content='文件信息:' + str(jsons) + "\n请手动上传",
            ssl=True,
        )
        m.send_mail()


# no_ack 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列
# True，无论调用callback成功与否，消息都被消费掉
channel.basic_consume("PDF-WATERMARK", callback,
                      auto_ack=True)
channel.start_consuming()
