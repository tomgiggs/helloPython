#encoding=utf8
import kafka
from kafka import KafkaProducer,KafkaConsumer

producer = KafkaProducer(bootstrap_servers="localhost:9092", linger_ms=500, acks=1)#127.0.0.1和localhost不一样？，使用localhost就能连接上，127.0.0.1连接不上。。。。
topic_name = 'flink_demo'
message = "this is a flinke demo,will it be ok?"
for i in range(200):
    producer.send(topic=topic_name, value=message)
producer.flush()
producer.close()
consumer = KafkaConsumer(bootstrap_servers='localhost:9092',group_id='test001')
consumer.subscribe("flink_demo")
for x in consumer:
    print(x)

