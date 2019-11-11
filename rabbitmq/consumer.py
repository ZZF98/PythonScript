# 消费者
import pika

# 连接
# auth info
auth = pika.PlainCredentials('guest', 'guest')  # auth info
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1', 5672, '/', auth))  # connect to rabbit
channel = connection.channel()  # create channel

# 申明队列
channel.queue_declare(queue='hello', durable=True, passive=True)


def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(body.decode())


# no_ack 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列
# True，无论调用callback成功与否，消息都被消费掉
channel.basic_consume("hello", callback,
                      auto_ack=False)
channel.start_consuming()
