#encoding=utf8
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

def classify():
    words = pandas.read_csv('D:\workspace\data\example.csv',sep='\t',usecols=['PROJ_NAME'],nrows=20)
    corpus = list(words['PROJ_NAME'].values.tolist())
    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
    word=vectorizer.get_feature_names()
    weight=tfidf.toarray()
    num_clusters = 4
    clf = KMeans(n_clusters=num_clusters)
    result = clf.fit(weight)
    s3 = clf.fit_predict(weight)
    print(s3)
    print(result) # KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300, n_clusters=4, n_init=10, n_jobs=None, precompute_distances='auto',random_state=None, tol=0.0001, verbose=0)
    # 20个中心点
    print(clf.cluster_centers_)
    print(result.labels_) #每个元素对应的标签 [0 1 0 1 0 3 0 2 0 1 0 1 0 0 0 0 0 0 0 0]
    print(result.labels_.shape)# 结果是一个(20,)的数组
    print(result.cluster_centers_.shape)#结果是一个4*23的矩阵，这是为什么呢，4个中心没问题，但为什么每个数组有23 个元素呢
    data_label = pandas.concat([pandas.DataFrame(corpus), pandas.Series(result.labels_)], axis = 1)
    print(data_label)
    data_label.columns = list(['Proj_name']) + [u'聚类类别']
    # data_label
    # 用来存储你的模型
    joblib.dump(clf, 'doc_cluster.pkl')
    km = joblib.load('doc_cluster.pkl')
    clusters = km.labels_.tolist()
    another_result01 = weight[result.labels_==2]
    print(another_result01)#另一种取元数据与标签的方式
    inertia = result.inertia_  # 获取聚类准则的总和
    print(inertia)

    num_count = pandas.Series(result.labels_).value_counts()
    data_center = pandas.DataFrame(result.cluster_centers_)
    result = pandas.concat([num_count,data_center],axis=1)
    # r = pandas.concat([corpus, pandas.Series(s.labels_, index=corpus.index)], axis=1)
    # print(r)
    terms = vectorizer.get_feature_names()
    # 每个样本所属的簇
    print(clf.labels_)
    i = 0
    while i < len(clf.labels_):
        # print(i, clf.labels_[i - 1])
        print(i, corpus[i], clf.labels_[i])
        i = i + 1
    print(clf.inertia_)
    films = {'title': corpus}

    frame = pandas.DataFrame(films, columns=[ 'title'])
    # km = joblib.load('doc_cluster.pkl')
    # clusters = km.labels_.tolist()
    order_centroids = clf.cluster_centers_.argsort()[:, ::-1]
    vocab_frame = pandas.DataFrame({'words': corpus})
    for i in range(num_clusters):
        print("Cluster %d words:" % i, end='')

        for ind in order_centroids[i, :3]:  # 每个聚类选 6 个词
            print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'))
        print()  # 空行
        print()  # 空行

        print("Cluster %d titles:" % i, end='')
        for title in frame.ix[i]['title'].values.tolist():
            print(' %s,' % title, end='')
