#encoding=utf8
#!/usr/bin/env python
'''
这个脚本用来检查rabbitmq，Redis及mysql的状态
@auth chenyilong
@date 2019.07.11 17:00
'''
import time
import os
import traceback
try:
    import pika
    import consul
    import redis
    import pymysql
    import traceback
except:
    try:
        os.system('pip install pika')
        os.system('pip install redis')
        os.system('pip install pymysql')
        os.system('pip install python-consul')
    except:
        traceback.print_exc()
        print('install python lib error exit!')
        exit(-1)

import pika
import redis
import pymysql
import consul #pip install python-consul

mysqlHost = '192.168.211.2'
redisHost= '192.168.211.2'
rabbitMqHost = '192.168.9.129'


def testRabbitMq():
    msg = 'Hello World! '
    try:
        user_pwd = pika.PlainCredentials("admin", "admin")
        connection =pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMqHost,credentials=user_pwd))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=msg)
        print('send msg :',msg,' success')
        connection.close()
    except:
        print('ooooooooooooooooh,rabbitmq connection error!')
        traceback.print_exc()

def testRedis():
    try:
        r = redis.Redis(host=redisHost, port=6379, db=0,password='Mm!Ou@S2e1R')
        cost = r.ping()
        # print(time.gmtime(r.time()[0]))
        print('redis say now is:',r.time())
        if cost:
            print('wooooooooooooooooow: redis running success!')
        else:
            print('redis not running or connection error')
    except:
        traceback.print_exc()

def testMysql():
    try:
        conn = pymysql.connect(host=mysqlHost, user='mmouser', passwd='Mm!Ou@S2e1R', db='vr_mmo', port=3306)
        cur = conn.cursor()
    except:
        print(traceback.print_exc())
        print('mysql connection error!')
        return
    try:
        sql = "SELECT CURDATE()"
        cur.execute(sql)
        result = cur.fetchall()
        for r in result:
            print('mysql say today is :',r[0])
        cur.close()
        conn.close()
        print('wooooooooooooooooow: mysql running success!')
    except:
        cur.close()
        conn.close()

def testConsule():
    consulClinet = consul.Consul('192.168.9.129',8500)
    index = None
    index, data = consulClinet.kv.get('esHost', index=index)
    print(data['Value'])
    consulClinet.kv.put('foo', 'bar')
    # consulClinet.agent.service.deregister()
    # consulClinet.agent.checks()
    print(consulClinet.agent.services())


testConsule()
# testRedis()
# testMysql()
# testRabbitMq()