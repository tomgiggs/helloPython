#encoding=utf8

import os
import time
# from gensim.models import Word2Vec # 这个用于训练模型，下面用于加载模型
from gensim.models import word2vec
# mopdelfilePath = 'E:\dataset\nlp\word2vec\sgns.zhihu.bigram' # 模型下载地址：https://github.com/Embedding/Chinese-Word-Vectors
# model = word2vec.Word2Vec.load(mopdelfilePath)
# print(model.wv['中国'])

# mopdelfilePath = 'E:/dataset/nlp/word2vec/sgns.zhihu.bigram' # 模型下载地址：https://github.com/Embedding/Chinese-Word-Vectors
mopdelfilePath = 'E:/dataset/nlp/word2vec/sgns.zhihu.bigram.bin'

from gensim.models import KeyedVectors
cn_model = KeyedVectors.load_word2vec_format(mopdelfilePath, binary=True) #这里路径要反斜杠，不知道为什么， 使用介绍：https://www.cnblogs.com/zhuxiang1633/p/10331618.htmlhttps://www.cnblogs.com/zhuxiang1633/p/10331618.html
# cn_model.save_word2vec_format('E:/dataset/nlp/word2vec/sgns.zhihu.bigram.bin',binary=True) #二进制占用空间比较小，而且加载速度快，不需要再次解析
print(cn_model['中国'])
print(cn_model.similarity('橙子','柑橘'))
print(cn_model.most_similar(positive='学历',topn=10))
# print(cn_model.wv.index2word )
from  numpy import linalg
import numpy as np
sent1_vec = (cn_model['中国']+cn_model['是']+cn_model['一个']+cn_model['伟大']+cn_model['的']+cn_model['国家'])/6
sent2_vec = (cn_model['中国']+cn_model['是']+cn_model['一个']+cn_model['强大']+cn_model['的']+cn_model['国家'])/6
sent1_vec = np.mat(sent1_vec)
sent2_vec = np.mat(sent2_vec)
print(sent1_vec)
# 计算余弦距离
num = sent1_vec.T * sent2_vec #若为行向量则 A * B.T
denom = linalg.norm(sent1_vec) * linalg.norm(sent2_vec) # 范数的计算工具：linalg.norm()
cos = num / denom #余弦值
print('===================')
print(cos)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
sim = 0.5 + 0.5 * cos #归一化
print(sim)