#encoding=utf8
#参考https://github.com/ljpzzz/machinelearning/blob/master/classic-machine-learning/matrix_factorization.ipynb这个做的spark推荐系统原型，使用jupyter notebook进行测试，
# 在spark运行过程中可以在jupyter notebook里面看到spark的输出日志,需要先配置好hadoop_home等环境变量再启动pyspark程序，不然容易出现问题
import os
import sys
#设置pyspark环境
os.environ['SPARK_HOME'] = "D:\program\spark2.4.2"
os.environ['PYSPARK_PYTHON'] = "D:\program\python3\python3.exe"
os.environ['HADOOP_HOME'] = "D:\program\hadoop-common-2.7.1-bin"
sys.path.append("D:\program\spark2.4.2\bin")
sys.path.append("D:programspark2.4.2\python")
sys.path.append("D:programspark2.4.2\python\pyspark")
sys.path.append("D:programspark2.4.2\python\lib")
sys.path.append("D:programspark2.4.2\python\lib\pyspark.zip")
sys.path.append("D:programspark2.4.2\python\lib\py4j-0.10.4-src.zip")
sys.path.append("D:\program\java8")
from pyspark import SparkContext
from pyspark import SparkConf

sc = SparkContext("local","testing")
print(sc) #如果正常打印出来的话就说明配置没问题
sc.stop() #退出pyspark
user_data = sc.textFile(r"E:\dataset\ml-20m\test.data") #需要进行数据清洗，数据补全，不然后面会出错
user_data.first()
rates = user_data.map(lambda x: x.split(",")[0:3])
print (rates.first())
from pyspark.mllib.recommendation import Rating
rates_data = rates.map(lambda x: Rating(int(x[0]),int(x[1]),int(x[2])))
print (rates_data.first())
from  pyspark.mllib.recommendation import ALS
from pyspark.mllib.recommendation import MatrixFactorizationModel
sc.setCheckpointDir('checkpoint/')
ALS.checkpointInterval = 2
model = ALS.train(ratings=rates_data, rank=20, iterations=5, lambda_=0.02) #这个步骤老是出现java.io.IOException: (null) entry in command string: null chmod 0644这种问题，需要添加合适的hadoop_home变量
print (model.predict(38,20))
print (model.recommendProducts(38,10))
# print (model.recommendUsers(20,10))
print (model.recommendUsers(1894476,10))
print (model.recommendProductsForUsers(3).collect())


