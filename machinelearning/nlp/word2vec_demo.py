#encoding=utf8
import re
import os
import json
import gensim
from gensim.models import word2vec
import jieba
import numpy as np
from scipy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity#余弦相似度计算
from nltk.tokenize import sent_tokenize#切句子的函数
from jieba.analyse import extract_tags #使用结巴提供的提取关键词的函数

from collections import Counter
from sklearn.cluster import KMeans


# model_file = './word2vec/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
# model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)


def sentence_vector(s,model):
    # words = jieba.lcut(s)
    # words = s.split(" ")
    words = s
    v = np.zeros(100)
    for word in words:
        try:
            v += model[word]  # 获取组成句子的所有单词的向量(每个向量为 100 维)，取这些向量的平均值来得到句子的向量
        except:
            pass
    v /= len(words)
    return v

def sent_similarity(v1, v2):
    # v1, v2 = sentence_vector(s1), sentence_vector(s2)
    return np.dot(v1, v2) / (norm(v1) * norm(v2))

def text_cleaner_v2(text=None):
    neg_file = open('../data/nltk_1000_neg_reviews.txt',"r")
    pos_file = open('../data/nltk_1000_pos_reviews.txt',"r")
    lines = []
    labels = []
    for line in neg_file.readlines():
        line = line.strip('\n')
        lines.append(line.split(' '))
        labels.append(0)
    for line in pos_file.readlines():
        line = line.strip('\n')
        lines.append(line.split(' '))
        labels.append(1)
    return lines, labels

def get_word2vec():
    contents,labels = text_cleaner_v2()
    bin_model_path = '../data/review_word2vec.model.bin'
    if not os.path.exists(bin_model_path):
        model = word2vec.Word2Vec(contents, min_count=1)
        model.wv.save_word2vec_format(bin_model_path, binary=True)
    else:
        model = gensim.models.KeyedVectors.load_word2vec_format(bin_model_path, binary=True)
    if not model:
        raise IOError
        return
    vec = []
    for line in contents:
        line_vec = []
        for word in line:
            line_vec.append(model[word])
            # print("most likely:",word,model.most_similar(word))
            #print("word vector: ".model[word])
        vec.append(line_vec)
        avg_matrix = sentence_vector(" ".join(line),model)
    return vec, labels

# get_word2vec()

def sent_distance():
    contents,labels = text_cleaner_v2()
    bin_model_path = '../data/review_word2vec.model.bin'
    if not os.path.exists(bin_model_path):
        model = word2vec.Word2Vec(contents, min_count=1)
        model.wv.save_word2vec_format(bin_model_path, binary=True)
    else:
        model = gensim.models.KeyedVectors.load_word2vec_format(bin_model_path, binary=True)
    if not model:
        raise IOError
        return
    lines_vec = []
    for line in contents:
        lines_vec.append(sentence_vector(line,model))
    print(sent_similarity(lines_vec[1],lines_vec[2]))
    #--------------------
    # print(np.dot(lines_vec[1], lines_vec[2]) / (norm(lines_vec[1]) * norm(lines_vec[2])))
    # print(line[1], line[2])

    return lines_vec, labels

sent_distance()

def classify_sent():
    contents,labels = text_cleaner_v2()
    bin_model_path = '../data/review_word2vec.model.bin'
    if not os.path.exists(bin_model_path):
        model = word2vec.Word2Vec(contents, min_count=1)
        model.wv.save_word2vec_format(bin_model_path, binary=True)
    else:
        model = gensim.models.KeyedVectors.load_word2vec_format(bin_model_path, binary=True)
    if not model:
        raise IOError
        return
    lines_vec = []
    for line in contents:
        lines_vec.append(sentence_vector(line,model))
    clf = KMeans(n_clusters=20)
    clf.fit(lines_vec)
    # print(clf.cluster_centers_)
    cls_labels = clf.labels_.tolist()
    # print(cls_labels)
    result_dict = {}
    index = 0
    for label in cls_labels:
        if str(label) not in result_dict:#需要将int转为str才能在字典中找到
            result_dict[str(label)] = []
        result_dict[str(label)].append(" ".join(contents[index])+"\n")
        index += 1
    # print(json.dumps(result_dict))
    for k in result_dict:
        print(len(result_dict[k]))