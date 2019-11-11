import json

import pika

# auth info
auth = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1', 5672, '/', auth))  # connect to rabbit
channel = connection.channel()

# 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
channel.exchange_declare(exchange='hello_fanout', durable=True, exchange_type='fanout')
for i in range(10):
    message = json.dumps({'OrderId': i})
    # 向队列插入数值 routing_key是队列名。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。routing_key 不需要配置
    channel.basic_publish(exchange='hello_fanout', routing_key='', body=message,
                          properties=pika.BasicProperties(delivery_mode=2))
    print(message)
connection.close()
