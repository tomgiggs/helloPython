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
        rclient.set(y[0], y[1])
        rclient.set(y, 5)

'''
windowns platform need winutils.exe and hadoop.dll ,without these ,a problem will raise, null\bin\winutils can not be found 
https://github.com/srccodes/hadoop-common-2.2.0-bin this url can provide the bin ,download it and config env var HADOOP_HOME and path and restart you ide ,problem will gone
'''
sc = SparkContext()
# 广播变量
# broadcast_var = sc.broadcast(array([1, 2, 3, 4]))
# print(broadcast_var.value)
# 数据切片
# cutted_data = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9], 3).glom().collect()
# print(cutted_data)
# # 读取文本数据
# fin = sc.textFile(r'd:\data\au_detail.csv')
# print(fin.glom().collect())
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

topic = {'data_cube_test':1}
'''
遇到找不到包的问题，到这里下载 http://search.maven.org/#search%7Cga%7C1%7Cspark-streaming-kafka-0-8-assembly
然后放到 python2.7/site-packages/pyspark-2.2.0-py2.7.egg/pyspark/jars下面即可解决
'''
kvs = KafkaUtils.createStream(ssc, '127.0.0.1:2181', "test_01", topic)
lines = kafka_strem_context.map(lambda x: x[1])
counts = lines.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a+b)
counts.pprint()
#kafka_strem_context.map(lambda x: x[1]).flatMap(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(out_data)
kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(lambda q:q.foreachPartition(toredis))
kafka_strem_context.map(out_data)
kafka_strem_context.map(lambda x: x[1]).count().saveAsTextFiles("/log/test_0",'.txt') # 这个基于流的写出文件的方法是可以运行的，但是如果不是基于流的sparkcontext就不行，原因未知
kafka_strem_context.map(lambda x: x[1]).saveAsTextFiles("/log/test_0",'.txt') #写出也为空只有一个_SUCCESS文件
kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).pprint()
# kafka_strem_context.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(out_data)
ssc.start()
ssc.awaitTermination()

#kafka_strem_context.flatMap(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(lambda q:q.foreachPartition(lambda u:rclient.set(u,5)))
sparkcontext.stop()
# test_csv_in.coalesce(1).write.mode(SaveMode.Overwrite).format("com.databricks.spark.csv").save("file:///D:/java_workspace/fun_test.csv")