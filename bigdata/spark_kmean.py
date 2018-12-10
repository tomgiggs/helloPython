#encoding=utf8
from numpy import array
from math import sqrt
from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans, KMeansModel
sc = SparkContext(appName='kafka_pyspark_test',)
# Load and parse the data
data = sc.textFile("D:\workspace\data\example.csv")
parsedData = data.map(lambda line:line)

# Build the model (cluster the data)
clusters = KMeans.train(parsedData, 2, maxIterations=10, initializationMode="random")

# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))

# Save and load model
clusters.save(sc, "D:\workspace\data\KMeansModel")
sameModel = KMeansModel.load(sc, "./model")
