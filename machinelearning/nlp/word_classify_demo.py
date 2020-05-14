#encoding=utf8
import json
import jieba
import jieba.posseg as pseg
import os
import sys
import pandas
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram, linkage
from sklearn.externals import joblib
from sklearn.cluster import KMeans

def get_content(row_num=2000):
    proj_names = []
    proj_name_df = pandas.read_csv(r'E:\dataset\secret\invest_info.csv',sep='\t',usecols=['PROJ_NAME'],nrows=row_num)
    raw_name = proj_name_df['PROJ_NAME'].tolist()
    for proj in proj_name_df['PROJ_NAME']:
        splited = " ".join(jieba.cut(proj))
        proj_names.append(splited)
    return proj_names, raw_name

# get_content()

def classify(num_clusters=20):
    corpus, raw_name = get_content()
    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
    weight = tfidf.toarray()
    clf = KMeans(n_clusters=num_clusters)
    clf.fit(weight)
    cls_labels = clf.labels_.tolist()
    result_dict = {}
    index = 0
    for label in cls_labels:
        if str(label) not in result_dict:  # 需要将int转为str才能在字典中打印出来
            result_dict[str(label)] = []
        result_dict[str(label)].append(raw_name[index])
        index += 1
    # print(json.dumps(result_dict))
    # 打印出来的结果就跟按中文排序的结果差不多，哈哈哈，搞了一堆花里胡哨的。。
    # for k in result_dict:
    #     for proj in result_dict[k]:
    #         print(proj)
    #要怎么获得每个聚类的关键词呢？把聚类中的文本再拿去切一遍计算出词频，截取前几个来当关键词？好像有一个聚类中心，是否可以拿来做一些处理？
    return result_dict

def classfy_old():
    corpus, raw_name = get_content()
    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
    weight = tfidf.toarray()
    num_clusters = 20
    clf = KMeans(n_clusters=num_clusters)
    result = clf.fit(weight)
    # s3 = clf.fit_predict(weight)
    # print(result.labels_) #每个元素对应的标签 [0 1 0 1 0 3 0 2 0 1 0 1 0 0 0 0 0 0 0 0]
    # print(result.cluster_centers_.shape)#结果是一个4*23的矩阵，这是为什么呢，4个中心没问题，但为什么每个数组有23 个元素呢
    # inertia = result.inertia_  # 获取聚类准则的总和
    # data_label = pandas.concat([pandas.DataFrame(corpus), pandas.Series(result.labels_)], axis=1,keys=("proj_name","tag"))
    # data_label.columns = list(['Proj_name']) + ['tag']
    # joblib.dump(clf, '../data/doc_cluster.pkl') # 保存模型,恢复使用clf = joblib.load('doc_cluster.pkl')
    # another_result01 = weight[result.labels_==2]#另一种取元数据与标签的方式
    member_count = pandas.Series(result.labels_).value_counts()#每个聚类的成员数量
    print(member_count)
    terms = vectorizer.get_feature_names()
    print(len(clf.cluster_centers_)) # 20个聚类中心，
    order_centroids = clf.cluster_centers_.argsort()[:, ::-1]
    vocab_frame = pandas.DataFrame({'words': terms})
    #不能用了，不知道什么改了。。。
    # for i in range(num_clusters):
    #     for ind in order_centroids[i, :3]:  # 每个聚类选 6 个词
    #         print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'))
    #     print("Cluster %d titles:" % i, end='')

classify()
# classfy_old()