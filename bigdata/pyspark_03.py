#encoding=utf8
from pyspark import SparkContext
from pyspark import SparkFiles
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def toredis(rdd):
    import redis
    rclient = redis.Redis(host="172.17.0.7", port=6379)
    # rdd.foreachPartition(lambda u: rclient.set(u, 5))
    for y in rdd:
        print(y)
        rclient.set(y[0], y[1])
        rclient.set(y, 5)



def toredis2(u):
    import redis
    rclient = redis.Redis(host="172.17.0.7", port=6379)
    rclient.set(u[0],u[1])
    for y in u:
        print(y)
        rclient.set(y, 5)


sparkcontext = SparkContext("spark://0.0.0.0:7077","spark_test01")

# spark = SparkSession \
#     .builder \
#     .appName("PythonWordCount") \
#     .getOrCreate()

result = sparkcontext.textFile('/pycode/test.txt')



sparkcontext.addPyFile('redis.zip')
lines = result.map(lambda x: x[1])
counts = result.map(lambda line: line.split("|@|")) \
    .map(lambda word: (word[0], word[2])) \
    .reduceByKey(lambda a, b: int(a)+int(b))
# result.map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a, b: int(a)+int(b)).foreachPartition(toredis)
counts.foreachPartition(toredis)
counts.saveAsTextFiles("/log/test.txt") #报错 AttributeError: 'PipelinedRDD' object has no attribute 'saveAsTextFiles'
counts.pprint()
#counts.map(lambda x: x[1]).map(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(lambda q:q.foreachPartition(toredis))
print("gooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooood")

sparkcontext.stop()



kafka_strem_context.flatMap(lambda x: (x.split("|@|")[0],x.split("|@|")[2])).reduceByKey(lambda a,b:a+b).foreachRDD(lambda q:q.foreachPartition(lambda u:rclient.set(u,5)))

# test_csv_in.coalesce(1).write.mode(SaveMode.Overwrite).format("com.databricks.spark.csv").save("file:///D:/java_workspace/fun_test.csv")


fin = open('xxx.cpmf').readlines()


