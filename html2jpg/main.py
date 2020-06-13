# -*- coding: utf-8 -*-
import base64
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import request

import cv2
import numpy as np
import pika
import requests
from PIL import ImageFont, ImageDraw, Image

# 图片大小
l = 300

# 登陆
address = 'localhost:5002'

auth = pika.PlainCredentials('guest', 'guest')  # auth info
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1', 5672, '/', auth))  # connect to rabbit
channel = connection.channel()  # create channel

queueName = 'WORD-REPORT-JPG-TEMPLATE'
# 申明队列
channel.queue_declare(queue=queueName, durable=True, passive=True)


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


def uploadJpg(key, new_name):
    # 重试三次
    for i in range(3):
        try:
            files = {"file": open(new_name, "rb")}
            # 超时时间为3分钟
            url = "http://{}/supervision/web/api/v3/unsecure/customer/upload/jpg?key={}".format(
                address, key)
            r = requests.post(url, headers="", files=files)
            if r.status_code == 200:
                if r.json()['data']:
                    print("upload jpg:" + r.text)
                    return True
                else:
                    print("失败")
            else:
                print("upload jpg no:" + r.text)
                continue
        except Exception as e:
            print(e)
            pass
    return False


# 回调
def callback(ch, method, properties, body):
    # 解析json
    jsons = json.loads(str(body.decode()))
    print(jsons)
    try:
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

        draw.text((229, 106), jsons["sterilizationDate"], font=font, fill=(60, 60, 60))
        draw.text((229, 189), jsons["sterilizationSn"], font=font, fill=(60, 60, 60))
        draw.text((267, 272), jsons["sterilizationPeriod"], font=font, fill=(60, 60, 60))
        draw.text((229, 345), jsons["sterilizationNumber"], font=font, fill=(60, 60, 60))
        draw.text((267, 416), jsons["chemicalDetection"], font=font, fill=(60, 60, 60))
        draw.text((267, 475), jsons["otherDetection"], font=font, fill=(60, 60, 60))
        draw.text((267, 537), jsons["processVariableDetection"], font=font, fill=(60, 60, 60))
        draw.text((229, 636), jsons["sterilizationStowage"], font=font, fill=(60, 60, 60))
        draw.text((267, 727), jsons["detectionType"], font=font, fill=(60, 60, 60))
        draw.text((229, 799), jsons["personnelName"], font=font, fill=(60, 60, 60))
        draw.text((229, 882), jsons["detectionMethod"], font=font, fill=(60, 60, 60))
        draw.text((229, 987), jsons["sterilizationPackagingType"], font=font, fill=(60, 60, 60))
        text = jsons["instrumentName"]
        instrumentName = ''
        if len(text) > 15:
            i = 0
            for txt in text:
                instrumentName = instrumentName + txt
                i = i + 1
                if i % 15 == 0:
                    instrumentName = instrumentName + "\n"

        draw.text((229, 1066), instrumentName, font=font, fill=(60, 60, 60))

        font = ImageFont.truetype(fontpath, 25)
        if '1' == jsons["type"]:
            draw.text((48, 1202), "物理检测", font=font, fill=(52, 52, 52))
            draw.text((48, 1592), "化学检测", font=font, fill=(52, 52, 52))
        else:
            draw.text((48, 1202), "生物检测", font=font, fill=(52, 52, 52))

        # 图片文字生成完毕
        # cv2.imshow("add_text", bk_img)
        # cv2.waitKey()
        bk_img = np.array(img_pil)
        cv2.imwrite("file.jpg", bk_img)
        print("图片文字生成完毕")
        if '1' == jsons["type"]:
            # 下载图片并进行图片合成
            # 解决竖屏方式
            request.urlretrieve(jsons["physicalPicUrl"], "test1.jpg")
            test1 = cv2.imread("test1.jpg")
            test1 = np.array(test1)
            cv2.imwrite("test1.jpg", test1)

            request.urlretrieve(jsons["chemicalPicUrl"], "test2.jpg")
            test2 = cv2.imread("test2.jpg")
            test2 = np.array(test2)
            cv2.imwrite("test2.jpg", test2)

            img1 = Image.open("test1.jpg")
            img2 = Image.open("test2.jpg")
            # x, y = img1.size[0], img1.size[1]
            img1_x, img1_y = img1.size
            img2_x, img2_y = img2.size
            h = img1_x / img1_y * l
            out1 = img1.resize((int(h), l), Image.ANTIALIAS)
            out1.save("test1.jpg")

            h2 = img2_x / img2_y * l
            out2 = img2.resize((int(h2), l), Image.ANTIALIAS)
            out2.save("test2.jpg")

            img1 = Image.open("test1.jpg")
            img2 = Image.open("test2.jpg")
            bk_img = Image.open("file.jpg")
            bk_img.paste(img1, (48, 1260, 48 + int(h), 1260 + l))
            bk_img.paste(img2, (48, 1670, 48 + int(h2), 1670 + l))

            bk_img.save("out.jpg")
            os.remove("test1.jpg")
            os.remove("test2.jpg")
        else:
            # 下载图片并进行图片合成
            request.urlretrieve(jsons["biologicalPicUrl"], "test1.jpg")
            test1 = cv2.imread("test1.jpg")
            test1 = np.array(test1)
            cv2.imwrite("test1.jpg", test1)
            img1 = Image.open("test1.jpg")
            # x, y = img1.size[0], img1.size[1]
            img1_x, img1_y = img1.size
            h = img1_x / img1_y * l
            out1 = img1.resize((int(h), l), Image.ANTIALIAS)
            # out1 = img1.resize((h_x, h_y), Image.ANTIALIAS)
            out1.save("test1.jpg")

            img1 = Image.open("test1.jpg")
            bk_img = Image.open("file.jpg")
            bk_img.paste(img1, (48, 1260, 48 + int(h), 1260 + l))
            bk_img.save("out.jpg")
            os.remove("test1.jpg")

        os.remove("file.jpg")
        print("图片生成完毕-----开始上传")
        data = uploadJpg(jsons["key"], "out.jpg")
        if data:
            os.remove("out.jpg")
        else:
            m = SendMail(
                username='xxxxxxxxxxxx@QQ.com',
                passwd='xxxxxxxxxxxx',
                recv=['xxxxxxxxxxxx@QQ.com'],
                title='JPG文件生成失败',
                content='文件信息:' + str(jsons),
                file=r"{" + 'contract.zip' + "}",
                ssl=True,
            )
            m.send_mail()
    except Exception as e:
        print(e)
        m = SendMail(
            username='xxxxxxxxxxxx@QQ.com',
            passwd='xxxxxxxxxxxx',
            recv=['xxxxxxxxxxxx@QQ.com'],
            title='JPG文件生成失败',
            content='文件信息:' + str(jsons) + "\n请手动上传",
            ssl=True,
        )
        m.send_mail()


# no_ack 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列
# True，无论调用callback成功与否，消息都被消费掉
channel.basic_consume(queueName, callback,
                      auto_ack=True)
channel.start_consuming()
