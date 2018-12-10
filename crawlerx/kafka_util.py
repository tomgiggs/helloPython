#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append('../')
reload(sys)
sys.setdefaultencoding('utf-8')
import os
# try:
#     import kafka
# except:
#     os.system('sudo pip install kafka')
#     import kafka
# try:
#     import lz4
# except:
#     os.system("sudo pip install lz4")
import traceback
import time
import json
from scrapy.utils.project import inside_project, get_project_settings
from scrapy_redis import connection, defaults
settings = get_project_settings()
from kafka import KafkaProducer
from redis import ConnectionError
import random
import threading
# import logging
# loger = logging.getLogger('s3_uploader')
# loger.setLevel(logging.DEBUG)
# fhandler = logging.FileHandler('../upload.log')
# shandler = logging.StreamHandler()
# loger.addHandler(shandler)
# loger.addHandler(fhandler)
lock = threading.Lock()
producer = KafkaProducer(bootstrap_servers="127.0.0.1:9092", linger_ms=500, acks=1)
def send_message(message, topic_name, partitions=0,**kwargs):
    status = False
    is_block = lock.acquire()
    while not is_block:
        is_block = lock.acquire()
    if is_block:
        try:
            # producer.send(topic=topic_name, value=message, partition=random.choice(range(partitions + 1)))
            # producer.send(topic=topic_name, value=message)
            producer.send(topic=topic_name,value=bytes(message.encode('utf-8'))) #Python3 要以这种方式发送，不然会报错误
            producer.flush()
            status = True
            lock.release()
        except:
            print(traceback.print_exc())
            status = False
            lock.release()

    #producer.flush()
    return status
