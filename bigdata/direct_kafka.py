#encoding=utf8
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import TopicAndPartition
from pyspark.streaming.kafka import KafkaUtils

def toredis(rdd):
    import redis
    rclient = redis.Redis(host="172.17.0.7", port=6379)
    for y in rdd:
        print(y)
        rclient.set(y[0], y[1])
        rclient.set(y, 5)


sparkcontext = SparkContext("spark://0.0.0.0:7077","spark_test01")
offsets = {}
part01 = TopicAndPartition('',2)
sparkcontext.addPyFile('redis.zip')
ssc = StreamingContext(sparkcontext, 5)

kafka_strem_context = KafkaUtils.createDirectStream(ssc, ['flumetest2'], {"metadata.broker.list": '172.17.0.6:9092','auto.offset.reset':'largest'})
kafka_strem_context.map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a, b: int(a)+int(b)).foreachRDD(lambda q:q.foreachPartition(toredis))
# kafka_strem_context.map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a, b: int(a)+int(b)).foreachPartition(toredis)# AttributeError: 'TransformedDStream' object has no attribute 'foreachPartition'

ssc.start()
ssc.awaitTermination()


#encoding=utf8
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import TopicAndPartition
from pyspark.streaming.kafka import KafkaUtils

def toredis(rdd):
    import redis
    rclient = redis.Redis(host="172.17.0.7", port=6379)
    for y in rdd:
        print(y)
        rclient.incrby(y[0],y[1])
        rclient.set(y, 5)


sparkcontext = SparkContext("spark://0.0.0.0:7077","spark_test01")
sparkcontext.addPyFile('redis.zip')
ssc = StreamingContext(sparkcontext, 5)

#kafka_strem_context = KafkaUtils.createDirectStream(ssc, ['flumetest2'], {"metadata.broker.list": '172.17.0.6:9092'})
kafka_strem_context = KafkaUtils.createDirectStream(ssc, ['flumetest2'], {"metadata.broker.list": '172.17.0.6:9092','auto.offset.reset':'largest'})
kafka_strem_context.map(lambda a:a[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a, b: int(a)+int(b)).foreachRDD(lambda q:q.foreachPartition(toredis))

ssc.start()
ssc.awaitTermination()