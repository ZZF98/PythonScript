# 生产者
import pika

# 连接
# auth info
auth = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1', 5672, '/', auth))  # connect to rabbit
channel = connection.channel()

"""
MQ默认建立的是临时 queue 和 exchange，如果不声明持久化，一旦 rabbitmq 挂掉，queue、exchange 将会全部丢失
所以一般在创建 queue 或者 exchange 的时候会声明 持久化
"""
# 声明消息队列，消息将在这个队列传递，如不存在，则创建,durable = True为持久化
channel.queue_declare(queue='hello')
"""
虽然 exchange 和 queue 都申明了持久化，但如果消息只存在内存里rabbitmq 重启后
内存里的东西还是会丢失。所以必须声明消息也是持久化，从内存转存到硬盘。
 properties=pika.BasicProperties(delivery_mode = 2))
"""
# 发送消息
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Flash22',
                      properties=pika.BasicProperties(delivery_mode=2))  # body是msg内容
connection.close()
