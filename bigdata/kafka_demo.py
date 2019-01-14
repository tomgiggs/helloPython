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
# ----------------------------------------------------
# #encoding=utf8
# from kafka import KafkaConsumer,TopicPartition
# # import time
# #
# # kclient = KafkaConsumer('ziniao_detail_result2', bootstrap_servers=["35.158.103.147:9092"], auto_offset_reset='latest',client_id='test01') #earliest
# # # for message in kclient:
# # #     print(message.value, message.topic)
# # # while True:
# # #     msg = kclient.poll(timeout_ms=5,max_records=10)   #从kafka获取消息
# # #     print msg
# # #     time.sleep(1)
# # print(kclient.topics())
# # # print(kclient.beginning_offsets([0]))
# # print(kclient.seek_to_beginning(topic='ziniao_detail_result2', partition=0))
# #
# #
# # print kclient.beginning_offsets(kclient.assignment())
# #
# import logging as log
# log.basicConfig(level=log.DEBUG)
#
# consumer = KafkaConsumer('ziniao_detail_result2', bootstrap_servers=["35.158.103.147:9092"], auto_offset_reset='earliest',group_id='test3',) #earliest ,enable_auto_commit=False
#
# #consumer.subscribe(topics=['ziniao_detail_result2',])
# # print consumer.topics()  #获取主题列表
# # print consumer.partitions_for_topic("ziniao_detail_result2")  #获取主题的分区信息  [0,1,2,3]
# # print consumer.subscription()  #获取当前消费者订阅的主题 # ['ziniao_detail_result2']
# print consumer.assignment()  #获取当前消费者topic、分区信息
# print consumer.beginning_offsets(consumer.assignment()) #获取当前消费者可消费的偏移量
# #print consumer.position(TopicPartition(topic='ziniao_detail_result2', partition=0))
# #print(consumer.beginning_offsets([TopicPartition(topic='ziniao_detail_result2', partition=0)])) # {TopicPartition(topic=u'ziniao_detail_result2', partition=0): 0}
# print(consumer.committed(TopicPartition(topic=u'ziniao_detail_result2', partition=0))) #committed 函数获取最后提交的offset，commit（）不需要参数
# consumer.unsubscribe()
#
# # print(consumer.subscribe(topics='ziniao_detail_result'))
# # print consumer.subscription()
# # print(consumer.assignment())
# # print(consumer.partitions_for_topic('ziniao_detail_result'))
# # #print(consumer.get_partition_offsets(topic='ziniao_detail_result',partition=1,request_time_ms=1000,max_num_offsets=10))
# #
# # #consumer.assign([TopicPartition(topic='ziniao_detail_result',partition=1),])
# # # print(consumer.position(TopicPartition(topic='ziniao_detail_result', partition='1')))
# # #print consumer.seek_to_beginning(TopicPartition(topic='ziniao_detail_result', partition=1))
# # #consumer.pause()
#
#
# #print consumer.beginning_offsets(consumer.assignment())
# #print(consumer.fetch_messages())
#
# consumer.assign([TopicPartition(topic='ziniao_detail_result', partition=1), ]) #assign 之前要先解除订阅 consumer.unsubscribe()
# #print(consumer.poll(max_records=10, timeout_ms=1000))
# print(consumer.assignment()) #只有assign后调用assign才有结果，
# print(consumer.position(TopicPartition(topic='ziniao_detail_result', partition=1))) #获取最新offset位置
#
# print(consumer.seek_to_end(TopicPartition(topic='ziniao_detail_result', partition=1)))
# print(consumer.seek_to_beginning()) #一般都是none
#
# #print consumer.beginning_offsets(TopicPartition(topic='ziniao_detail_result', partition=1))
#
#
# #consumer.seek(TopicPartition(topic='ziniao_detail_result2', partition=0), 0)  #重置偏移量，从第5个偏移量消费
# for message in consumer:
#
#     # ziniao_detail_result2:0:8: key=None value={}
#     print(message)
#     print(message.offset) #ConsumerRecord(topic=u'ziniao_detail_result2', partition=0, offset=8, timestamp=1531550762462L, timestamp_type=0, key=None, value=' ', checksum=None, serialized_key_size=-1, serialized_value_size=2735)
#
#     #consumer.commit()
# #
# # import os
# # try:
# #     import lz4
# # except:
# #     os.system("sudo pip install lz4")
