import pika

# 连接
# auth info
auth = pika.PlainCredentials('guest', 'guest')  # auth info
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1', 5672, '/', auth))  # connect to rabbit
channel = connection.channel()  # create channel

# 创建临时队列，consumer关闭后，队列自动删除
result = channel.queue_declare('', exclusive=True)
# 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
channel.exchange_declare(exchange='hello_fanout', durable=True, exchange_type='fanout')
# 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去
channel.queue_bind(exchange='hello_fanout', queue=result.method.queue)


# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(body.decode())


channel.basic_consume(result.method.queue, callback,
                      # 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
                      False)
channel.start_consuming()
