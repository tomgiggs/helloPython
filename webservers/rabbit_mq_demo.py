#!/usr/bin/env python
import pika

user_pwd = pika.PlainCredentials("admin", "admin")
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMqHost, credentials=user_pwd))
connection = pika.BlockingConnection(parameters=(pika.ConnectionParameters(host='192.168.9.129',credentials=user_pwd)))
channel = connection.channel()
for method_frame, properties, body in channel.consume('hello'):
    print(method_frame, properties, body)
    channel.basic_ack(method_frame.delivery_tag)
    if method_frame.delivery_tag == 10:
        break
requeued_messages = channel.cancel()
print('Requeued %i messages' % requeued_messages)
connection.close()


#----------rabbitmq sender-------------
# try:
#     connection = pika.BlockingConnection(parameters=(pika.ConnectionParameters(host=rabbitMqHost)))
#     channel = connection.channel()
#     for method_frame, properties, body in channel.consume('hello'):
#         print(method_frame, properties, body)
#         channel.basic_ack(method_frame.delivery_tag)
#         if method_frame.delivery_tag == 10:
#             break
#     requeued_messages = channel.cancel()
#     print('Requeued %i messages' % requeued_messages)
#     connection.close()
# except:
#     print('ooooooooooooooooh,rabbitmq connection error!')
#     traceback.print_exc()

# connection =pika.BlockingConnection(pika.ConnectionParameters(host='192.168.9.129'))
# channel = connection.channel()
# channel.queue_declare(queue='hello')
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World! 222222222222222222222222222222')
# print(" [x] Sent 'Hello World!'")
# connection.close()
