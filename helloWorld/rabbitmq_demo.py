import os
import argparse
try:
    import pika
    import traceback
except:
    try:
        os.system('pip install pika')
        import pika
    except:
        traceback.print_exc()
        print('install python lib error exit!')
        exit(-1)

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

def fanout_consume():
    user_pwd = pika.PlainCredentials("edboxRabbitmq-beta-cn", "rabbitmq123abc@edbox-beta-cn")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq-tncj.edbox-beta-cn.101.com", credentials=user_pwd,port=5672,virtual_host='edboxBetaCn'))
    channel = connection.channel()
    channel.exchange_declare('exchange.username.beta-cn', 'fanout', durable=True)
    # 不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
    result = channel.queue_declare("edbox_test",exclusive=True)
    queue_name = result.method.queue
    print("queuename is:", queue_name)
    channel.queue_bind(exchange='exchange.username.beta-cn', queue=queue_name)
    print(' [*] Waiting for msg. To exit press CTRL+C')
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()

def basic_publish():
    msg = '{"name":"111111"} '
    rabbitMqHost = ""
    rabbitMqUser = ""
    rabbitMqPasswd = ""
    try:
        user_pwd = pika.PlainCredentials(rabbitMqUser,rabbitMqPasswd)
        connection =pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMqHost,credentials=user_pwd))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='', routing_key='hello', body=msg)
        print('send msg :', msg, ' success')
        connection.close()
    except:
        print('ooooooooooooooooh,rabbitmq connection error!')
        traceback.print_exc()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbhost', default='localhost')
    parser.add_argument('--dbport', default=3306, type=int)
    parser.add_argument('--dbuser', default='root')
    parser.add_argument('--dbpasswd', help='user password')
    parser.add_argument('--daybefore', default=14, type=int)
    args = parser.parse_args()
    fanout_consume()

# python del_tars_log_table.py  --dbhost xxxx --dbpasswd xxxx

