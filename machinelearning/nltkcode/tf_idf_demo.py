# coding:utf-8
import copy
import jieba
from sklearn.feature_extraction.text import CountVectorizer#统计词频
from sklearn.feature_extraction.text import TfidfTransformer#计算反转词频
# 以三个单引号括起来得到字符串''''''在结巴分词中会遇到编码问题，用双引号的就不会。。。
#获取一段文字中的关键词,module 'jieba' has no attribute 'analyse'
# sentence= "相关公司股票走势 新野纺织 全景网8月21日讯 新野纺织 (002087)周三晚间发布公告,公司于近日收到财政拨付的2013年第一季度贷款利差补贴合计751.63万元,根据规定,该笔政府补助将确认为营业外收入。 "
# keywords = jieba.analyse.extract_tags(sentence, topK=20, withWeight=True, allowPOS=('n','nr','ns'))
# print(keywords)

#--------------------
#获取一批文章中的关键词
corpus =open(r"E:\dataset\sohu-20130820-20161031\20130821",encoding='utf8').readlines()
contents = []
for line in corpus:
    content = line.split('`1`2')[2]
    contents.append(' '.join(jieba.cut(content,cut_all=True)))
stopwords = open('./stop_words_zh_utf8.txt','r',encoding='utf8').readlines()
vectorizer = CountVectorizer(stop_words=stopwords)
#计算每个词语出现的次数，contents里面的所有元素都会使用空格切词，然后得到一个词袋（所有文档的所有单词组成），每个文档出现的词会在词袋中标明位置和数值，所以可能会有几百万个列
freq = vectorizer.fit_transform(contents)
#获取词袋中所有的词
word = vectorizer.get_feature_names()
# print(word)
#查看每个文档每个词出现的次数
freq_table = freq.toarray()
print(freq_table)
transformer = TfidfTransformer()
#将词频矩阵freq统计成TF-IDF值
tfidf = transformer.fit_transform(freq)
transformer.use_idf
#查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
# print(tfidf.toarray())
#---------------
#根据反转词频来获取关键词，这种方式虽然可以计算出关键词标签，但是好像是比较麻烦的，这个是取前8个，要不设置一个阈值试看看？
# j=0
# for doc_freq in tfidf.toarray():
#     raw_doc_freq = copy.deepcopy(doc_freq)
#     doc_freq.sort()
#     valve = doc_freq[-8]
#     word_index = []
#     i = 0
#     for freq in raw_doc_freq:
#         if freq >=valve:
#             word_index.append(i)
#         i+=1
#     for index in word_index:
#         print(word[index])
#     print(doc_freq[-8:])
#     print(contents[j])
#     j+=1
#     if j>20:
#         break
# print('-------------------------------------------------------------------')
#使用阈值来获得关键词，得到的结果有的很少，有得很多，有的关键词不是核心关键词
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
        print(word[index])
    j+=1
    if j>20:
        break
print('-------------------------------------------------------------------')

#--------------------
#根据词频来获取关键词,这个打出来的词会多于8个，而且会有不少不是名词的单词，比如表示，比较等
# j=0
# for doc_freq in freq_table:
#     print(contents[j])
#     raw_doc_freq = copy.deepcopy(doc_freq)
#     doc_freq.sort()
#     valve = doc_freq[-8]
#     word_index = []
#     i = 0
#     for freq in raw_doc_freq:
#         if freq >=valve:
#             word_index.append(i)
#         i+=1
#     for index in word_index:
#         print(word[index])
#     print(doc_freq[-8:])
#     j+=1
#     if j>20:
#         break
