# encoding=utf8
import pickle
from sklearn.externals import joblib
from sklearn import datasets
import pandas
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import os.path

dataset_path = r'E:\dataset\ml-20m'

pandas.set_option('display.max_rows',500)
pandas.set_option('display.max_columns',500)
pandas.set_option('display.width',1000)
source = pandas.read_csv(os.path.join(dataset_path,"ratings20000.csv"),sep=",",nrows=50000)
print(source.head())

'''
首先想一下我想要做什么：
我想知道一个用户对一个电影的评分预测，那我需要怎么处理csv数据呢？
做训练需要一组输入，一组标签，我要以哪一列为标签呢？在这里我想知道用户对电影的评分，那标签应该就是电影ID了，不过这个跟iris数据不一样，iris是四个列（参数）确定一个标签，这个电影数据用户与电影ID是没有关系的，而且有比较强的主观性
推荐数据跟推理性的数据不太一样，如果里面的列增加几个电影标签相关的列是不是做起来更简单？这么说来推荐类数据好像不适合使用sklearn做？或者说推荐出来的不太科学？

'''
target_data = source.pop('rating')
from sklearn.model_selection import train_test_split
train_X, test_X, train_y, test_y = train_test_split(source, target_data,train_size=0.8,test_size=0.2,random_state=50)

target_df = pandas.DataFrame({'rating':target_data})#需要先重组成dataframe，不然会报错
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB

print('-------------knn model ----------------')
knn_clf = KNeighborsClassifier().fit(train_X, train_y.astype('int'))
pred_y01 = knn_clf.predict(test_X)
print(pred_y01)
print(test_y)
print('model score is：',knn_clf.score(test_X, test_y.astype('int')))





