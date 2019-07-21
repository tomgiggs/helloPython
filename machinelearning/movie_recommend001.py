#encoding=utf8
'''
通过相似用户来给用户推荐电影UserCF
'''
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
source = pandas.read_csv(os.path.join(dataset_path,"ratings20000.csv"),sep=",",nrows=500)
print(source.head()) #    userId  movieId  rating   timestamp
#使用postgresql进行数据初步分析统计：SELECT userid,count(*),json_agg(movieid) FROM movie_lens.user_record group by userid limit 20 

