#encoding=utf8
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
# from pyspark.sql import SparkSession

def toredis(rdd):
    import redis
    rclient = redis.Redis(host="172.17.0.7", port=6379)
    # rdd.foreachPartition(lambda u: rclient.set(u, 5))
    rclient.set(','.join(rdd.collect()),5)
    return
    for y in u:
        print(y)
        rclient.set(y, 5)


def toredis2(u):
    import redis
    rclient = redis.Redis(host="172.17.0.7", port=6379)
    rclient.set(u[0],u[1])
    for y in u:
        print(y)
        rclient.set(y, 5)


sparkcontext = SparkContext("spark://0.0.0.0:7077","spark_test01")


sparkcontext.textFile('/pycode/test.txt')

sparkcontext.addPyFile('redis.zip')
ssc = StreamingContext(sparkcontext, 5)
propertites={
    'bootstrap.servers':'172.17.0.6:9092',
    "auto.offset.reset": "largest",
    'group.id':'test001',
}
kafka_strem_context = KafkaUtils.createStream(ssc,"172.17.0.6:2181","spark_test12",{"flumetest2":1},kafkaParams=propertites)
def out_data(y):
    print(y)


lines = kafka_strem_context.map(lambda x: x[1])
counts = lines.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a+b)
counts.pprint()
#kafka_strem_context.map(lambda x: x[1]).flatMap(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(out_data)
kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(lambda q:q.foreachPartition(toredis))
kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(lambda q:q.foreachPartition(toredis))
print("gooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooood")


kafka_strem_context.map(out_data)
kafka_strem_context.map(lambda x: x[1]).count().saveAsTextFiles("/log/test_0",'.txt') # 这个基于流的写出文件的方法是可以运行的，但是如果不是基于流的sparkcontext就不行，原因未知




kafka_strem_context.map(lambda x: x[1]).saveAsTextFiles("/log/test_0",'.txt') #写出也为空只有一个_SUCCESS文件
kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).pprint()


# result = kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b)

# kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(toredis)
# kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(out_data)


ssc.start()
ssc.awaitTermination()

#kafka_strem_context.flatMap(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(lambda q:q.foreachPartition(lambda u:rclient.set(u,5)))

# test_csv_in.coalesce(1).write.mode(SaveMode.Overwrite).format("com.databricks.spark.csv").save("file:///D:/java_workspace/fun_test.csv")