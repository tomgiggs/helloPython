#encoding=utf8
#python3 不允许在函数内import了SyntaxError: import * only allowed at module level
import os
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.data.path.append(r'E:\dataset\nltk_data') #指定nltk数据集的位置，不然默认是在C盘或者D盘等盘符根目录找ntlk_data的
from nltk.corpus import movie_reviews
import jieba
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA#主成分分析，用来对数据进行降维
from sklearn import svm
from sklearn import metrics
import jieba
from sklearn.feature_extraction.text import CountVectorizer#统计词频
from sklearn.feature_extraction.text import TfidfTransformer#计算反转词频
from sklearn.model_selection import train_test_split
from gensim.models import word2vec
import gensim
from sklearn.manifold import TSNE
from matplotlib.font_manager import *
import matplotlib.pyplot as plt

def classfy_by_nltk():
    view = ["Great place to be when you are in Bangalore",
            "The place was being renovated when I visited so the seating was limited",
            "Loved the ambience, loved the food",
            "The place is not easy to locate"]
    sid = SentimentIntensityAnalyzer()
    for sen in view:
        print(sen)
        ss = sid.polarity_scores(sen)
        for k in ss:
            print('{0}:{1},\n'.format(k, ss[k]), end='')

def read_movie_data_v1():
    positive_fileids = movie_reviews.fileids('pos')  # list类型 1000条数据 每一条是一个txt文件
    print(len(positive_fileids))
    pos_reviews = []
    for review_name in positive_fileids:
        pos_review = movie_reviews.words(fileids=[review_name])
        pos_reviews.append(pos_review)

def read_movie_data_v2():
    root_dir = r'E:\dataset\nltk_data\corpora\movie_reviews'
    folders = ['neg', 'pos']
    for foldername in folders:
        out_file = '../data/nltk_1000_' + foldername + '_reviews.txt'  # 输出文件
        output = open(out_file, 'w')
        rootdir = root_dir + '\\' + foldername
        for parent, dirnames, filenames in os.walk(rootdir):
            for filename in filenames:
                content = open(rootdir + '\\' + filename).read()
                line = re.sub("[:\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", content).replace("\n", " ").replace("\t", " ").replace("  ", " ")
                output.writelines(line+'\n')
        output.close()

# read_movie_data_v2()

def text_cleaner(text=None):
    neg_file = open('../data/nltk_1000_neg_reviews.txt',"r")
    pos_file = open('../data/nltk_1000_pos_reviews.txt',"r")
    lines = []
    labels = []
    for line in neg_file.readlines():
        line = re.sub("[:\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line).replace("\n"," ").replace("\t"," ").replace("  "," ")
        lines.append(line)
        labels.append(0)
    for line in pos_file.readlines():
        line = re.sub("[:\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line).replace("\n", " ").replace(
            "\t", " ").replace("  ", " ")
        lines.append(line)
        labels.append(1)
        # word_list = jieba.cut(line, cut_all=True)
        # print(" ".join([word for word in word_list]))

    return lines, labels

def text_cleaner_v2(text=None):
    neg_file = open('../data/nltk_1000_neg_reviews.txt',"r")
    pos_file = open('../data/nltk_1000_pos_reviews.txt',"r")
    lines = []
    labels = []
    for line in neg_file.readlines():
        line = re.sub("[:\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line).replace("\n"," ").replace("\t"," ").replace("  "," ")
        lines.append(line.split(' '))
        labels.append(0)
    for line in pos_file.readlines():
        line = re.sub("[:\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line).replace("\n", " ").replace(
            "\t", " ").replace("  ", " ")
        lines.append(line.split(' '))
        labels.append(1)
        # word_list = jieba.cut(line, cut_all=True)
        # print(" ".join([word for word in word_list]))

    return lines, labels

def cal_emotion_by_idf():
    contents,labels = text_cleaner()
    # train_contents, train_labels, test_contents, test_lables = train_test_split(contents, labels, train_size=0.8, test_size=0.2, random_state=50)
    stopwords = open('./stop_words_en.txt', 'r', encoding='utf8').readlines()
    vectorizer = CountVectorizer(stop_words=stopwords)
    freq = vectorizer.fit_transform(contents)
    freq_array = freq.toarray()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(freq)
    idf_array = tfidf.toarray()
    pca = PCA(n_components=200)
    # review_motion = pca.fit(idf_array)
    review_motion = pca.fit_transform(idf_array)
    # SVM分类
    clf = svm.SVC(C=2.0, probability=True)
    clf.fit(review_motion, labels)
    print('Test Accuracy is: %.2f' % clf.score(review_motion, labels))

def cal_emotion_by_word2vec():
    contents_vec, labels = get_word2vec()
    pca = PCA(n_components=200)
    # review_motion = pca.fit(idf_array)
    review_motion = pca.fit_transform(contents_vec)
    # SVM分类
    clf = svm.SVC(C=2.0, probability=True)
    clf.fit(review_motion, labels)
    print('Test Accuracy is: %.2f' % clf.score(review_motion, labels))


def get_word2vec():
    contents,labels = text_cleaner_v2()
    model_path = 'review_word2vec.model'
    bin_model_path = 'review_word2vec.model.bin'
    model = None
    if not os.path.exists(bin_model_path):
        model = word2vec.Word2Vec(contents, min_count=1)
        # model.save(model_path)
        model.wv.save_word2vec_format(bin_model_path, binary=True)
    else:
        # model = word2vec.Word2Vec.load(model_path)
        model = gensim.models.KeyedVectors.load_word2vec_format(bin_model_path, binary=True)
    # print(model['good'])
    # sim = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=5)
    # sim = model.wv.similarity("woman", "man")
    # print(sim)
    if not model:
        raise IOError
        return
    vec = []# lines-->line--->words---->word---->similarWords
    for line in contents:
        line_vec = []
        for word in line:
            #model[word] 这是与最相近的100个词的余弦距离吗？跟命令行版本的word2vec有点不一样啊
            line_vec.append(model[word])
        vec.append(line_vec)
    return vec, labels

'''
可视化数据分布，用户观察数据特征
'''
def show_sim_graph():
    contents,labels = text_cleaner_v2()
    bin_model_path = 'review_word2vec.model.bin'
    model = None
    if not os.path.exists(bin_model_path):
        model = word2vec.Word2Vec(contents, min_count=1)
        model.wv.save_word2vec_format(bin_model_path, binary=True)
    else:
        model = gensim.models.KeyedVectors.load_word2vec_format(bin_model_path, binary=True)
        #如果想往里面添加新的数据进行训练要做做呢？ model.update_vocab([])？

    X_tsne = TSNE(n_components=2, learning_rate=100).fit_transform(model.wv[contents[0]])
    # 解决负号'-'显示为方块的问题
    plt.figure(figsize=(14, 8))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
    for i in range(len(X_tsne)):
        x = X_tsne[i][0]
        y = X_tsne[i][1]
        plt.text(x, y, contents[i],  size=16)
    plt.show()
    pass

# get_word2vec()
# cal_emotion_by_word2vec()
# show_sim_graph()

# text_cleaner()
# cal_emotion()

