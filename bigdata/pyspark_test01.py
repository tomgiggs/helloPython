#encoding=utf8
# import pyspark
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pandas
# import numpy
from numpy import array
import sys

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

ssc = StreamingContext(sc, 1)

topic = {'data_cube_test':1}
'''
遇到找不到包的问题，到这里下载 http://search.maven.org/#search%7Cga%7C1%7Cspark-streaming-kafka-0-8-assembly
然后放到 python2.7/site-packages/pyspark-2.2.0-py2.7.egg/pyspark/jars下面即可解决
'''
kvs = KafkaUtils.createStream(ssc, '127.0.0.1:2181', "test_01", topic)
lines = kvs.map(lambda x: x[1])
counts = lines.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a+b)
counts.pprint()

ssc.start()
ssc.awaitTermination()
