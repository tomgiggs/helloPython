# coding:utf-8
import copy
import os
import pickle
import traceback
from sklearn.preprocessing import LabelEncoder#标签编码, encoded_labels = labelEncoder.fit_transform(labels)
import jieba
from sklearn.feature_extraction.text import CountVectorizer#统计词频
from sklearn.feature_extraction.text import TfidfTransformer#计算反转词频
'''
以三个单引号括起来得到字符串''''''在结巴分词中会遇到编码问题，用双引号的就不会。。。
获取一段文字中的关键词,module 'jieba' has no attribute 'analyse'
如何保存tfidf的计算结果呢，如何在下次有新的输入时利用上次计算得到的结果来加快计算呢？
sentence= "相关公司股票走势 新野纺织 全景网8月21日讯 新野纺织 (002087)周三晚间发布公告,公司于近日收到财政拨付的2013年第一季度贷款利差补贴合计751.63万元,根据规定,该笔政府补助将确认为营业外收入。 "
keywords = jieba.analyse.extract_tags(sentence, topK=20, withWeight=True, allowPOS=('n','nr','ns'))
print(keywords)
'''


#获取一批文章中的关键词
def get_data_content():
    corpus =open(r"E:\dataset\sohu-20130820-20161031\20130821",encoding='utf8').readlines()
    contents = []
    for line in corpus:
        content = line.split('`1`2')[2]
        contents.append(' '.join(jieba.cut(content,cut_all=True)))
    return contents

def cal_tfidf(contents):
    # contents = get_data_content()
    model_path = 'tfidf_train_model.pkl'
    stopwords = open('./stop_words_zhcn.txt','r',encoding='utf8').readlines()
    vectorizer = None
    try:
        vectorizer = pickle.load(open(model_path, "rb"))
    except:
        traceback.print_exc()
    if not vectorizer:
        vectorizer = CountVectorizer(stop_words=stopwords)
        #计算每个词语出现的次数，contents里面的所有元素都会使用空格切词，然后得到一个词袋（所有文档的所有单词组成），每个文档出现的词会在词袋中标明位置和数值，所以可能会有几百万个列
    freq = vectorizer.fit_transform(contents)
    keyword_freq = vectorizer.vocabulary_ #每个词出现的次数
    print(keyword_freq)
    word = vectorizer.get_feature_names()#获取词袋中所有的词
    # print(word)
    freq_table = freq.toarray()    #查看每个文档每个词出现的次数
    # print(freq_table)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(freq)    #将词频矩阵freq统计成TF-IDF值
    if not os.path.exists(model_path):
        with open(model_path, 'wb') as fw:
            pickle.dump(vectorizer.vocabulary_, fw) #保存模型

    # print(tfidf.toarray())  # 查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    # transformer.use_idf
    return tfidf

#根据反转词频来获取关键词，这种方式虽然可以计算出关键词标签，但是好像是比较麻烦的，这个是取前8个，要不设置一个阈值试看看？
def get_idf_keyword(n,tfidf,words,contents):
    j=0
    for doc_freq in tfidf.toarray():
        raw_doc_freq = copy.deepcopy(doc_freq)
        doc_freq.sort()
        valve = doc_freq[-n]
        word_index = []
        i = 0
        for freq in raw_doc_freq:
            if freq >=valve:
                word_index.append(i)
            i+=1
        for index in word_index:
            print(words[index])
        print(doc_freq[-n:])
        print(contents[j])
        j+=1
        if j>20:
            break
    print('-------------------------------------------------------------------')

# #使用阈值来获得关键词，得到的结果有的很少，有得很多，有的关键词不是核心关键词
def get_valve_keyword(n,tfidf,words,contents):
    j=0
    valve = 0.188888
    for doc_freq in tfidf.toarray():
        print(contents[j])
        word_index = []
        i = 0
        for freq in doc_freq:
            if freq >= valve:
                word_index.append(i)
            i+=1
        for index in word_index:
            print(words[index])
        j+=1
        if j>20:
            break
    print('-------------------------------------------------------------------')

#根据词频来获取关键词,这个打出来的词会多于8个，而且会有不少不是名词的单词，比如表示，比较等
def get_freq_keyword(words,freq_table,contents):
    j=0
    for doc_freq in freq_table:
        print(contents[j])
        raw_doc_freq = copy.deepcopy(doc_freq)
        doc_freq.sort()
        valve = doc_freq[-8]
        word_index = []
        i = 0
        for freq in raw_doc_freq:
            if freq >=valve:
                word_index.append(i)
            i+=1
        for index in word_index:
            print(words[index])
        print(doc_freq[-8:])
        j+=1
        if j>20:
            break

def simple_keyword(content):
    stopwords = open('./stop_words_zhcn.txt','r',encoding='utf8').readlines()
    vectorizer = CountVectorizer(stop_words=stopwords)
    freq = vectorizer.fit_transform(content)
    keyword_freq = vectorizer.vocabulary_ #每个词出现的次数
    print(len(keyword_freq),keyword_freq)
    # for k,v in keyword_freq.items():
    #     print(k,v)
    freq_topn = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
    print("word freq topN result:{}".format(freq_topn[:10]))
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(freq)
    words = vectorizer.get_feature_names()
    # print("word num:{},detail info:{}".format(len(transformer.idf_), transformer.idf_))
    # print(len(tfidf.toarray()[0]))
    # print(len(words))
    #从上面的结果可以看出 len(tfidf.toarray()[0])===len(words)
    idf_dict = dict(zip(words, tfidf.toarray()[0]))
    idf_topn = sorted(idf_dict.items(), key=lambda x: x[1], reverse=True)
    print("word idf topN result:{}".format(idf_topn[:10]))
    #单独一个句子切关键词得到的topn结果都不理想，但是相对频率统计来说，idf的效果是会好一点的

def advance_keyword(contents):
    stopwords = open('./stop_words_zhcn.txt','r',encoding='utf8').readlines()
    vectorizer = CountVectorizer(stop_words=stopwords)
    freq = vectorizer.fit_transform(contents)
    keyword_freq = vectorizer.vocabulary_ #每个词出现的次数
    print(len(keyword_freq),keyword_freq)
    freq_topn = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
    print("word freq topN result:{}".format(freq_topn[:10]))
    words = vectorizer.get_feature_names()
    #使用词频来计算关键词
    for line_freq in freq:
        line_dict = {}
        i = -1
        for word_freq in line_freq.toarray()[0]:
            i += 1
            if word_freq==0:
                continue
            line_dict[words[i]] = word_freq
        line_topn = sorted(line_dict.items(), key=lambda x: x[1], reverse=True)
        print("word freq topN result:{}".format(line_topn[:10]))#从这里就可以看出效果比单纯一段话做关键词提取好
        break

    #使用idf来计算关键词
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(freq)
    idf_dict = dict(zip(words, tfidf.toarray()[0]))
    idf_topn = sorted(idf_dict.items(), key=lambda x: x[1], reverse=True)
    print("word idf topN result:{}".format(idf_topn[:10]))
    for line_idf in tfidf:
        line_dict = {}
        i = -1
        for word_idf in line_idf.toarray()[0]:#这里line_idf是一个很有趣的结构，就算一直取[0][0]这样还是自身，需要转成数组后才能顺利迭代元素
            i += 1
            if word_idf == 0:
                continue
            print(word_idf)
            line_dict[words[i]] = word_idf
        line_topn = sorted(line_dict.items(), key=lambda x: x[1], reverse=True)
        print("word freq topN result:{}".format(line_topn[:10]))#从这里就可以看出效果比单纯一段话做关键词提取好
        break
        #同样这里idf的效果还是好于简单词频统计的，但是已经没有很明显的区别了

'''
上面advance_keyword效果差不多可以满足简单使用了，但是在实际应用中如果新增了预料那就会引起词频的变化，这个变化会不会有一个上限，
就是到达一定数量后就趋于稳定，词频变化很小，不然每次有新增文章就会引起关键词变化，那计算量应该会变得很庞大。
实际应用中应该可以先做一下聚类分析，把文本初步分为几十类，然后再同一个分组内做关键词提取，那样准确率应该还会有不少提高。
还有一个提取关键词的方式是使用word2vec，但是这个还没想好怎么处理，理论上word2vec训练好后就可以保持一段时间很稳定了
对于聚类分析还有一个就是找到有标签的数据，使用机器学习模型进行计算与预测，不过这里主要是做关键词提取，后面专门写一个做文本聚类分析的
'''

def main():
    sents = get_data_content()
    # simple_keyword([sents[1]])
    advance_keyword(sents)
    pass

main()
