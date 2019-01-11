# _*_coding:utf-8_*_
'''
所属行业分类器
'''

import random
import json
import re
import os
import fasttext
import jieba
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"industry_id_model.bin")
print(model_path)

def seg_text(text):
    return " ".join(jieba.cut_for_search(text))


def process_train_input():
    r = []
    x = []
    with open("industry_default_data.txt", 'r', encoding='gb18030') as f,open("industry_default.dat", "w", encoding='utf-8') as industry_default_fa:
        for line in f:
            line = line.strip('\n')
            cols = line.split('\t')
            if len(cols) == 2:
                text, label = cols
                r.append([text, label])
        for text, label in r:
            if random.random() < 0.9:
                label = "__label__" + label
                text = seg_text(text)
                x.append([text, label])
                print(text, label, file=industry_default_fa)

def train_model():
    process_train_input()
    print("training,please wait a monent  ...")
    classifier = fasttext.supervised("industry_default.dat", "industry_default_model", label_prefix="__label__",
                                     epoch=40, dim=50, bucket=2000000, word_ngrams=4, lr=0.2)


def predict_model(proj_name):
    classifier = fasttext.load_model("industry_default_model.bin", label_prefix='__label__')
    st = []
    ot = []
    st.append(seg_text(proj_name))
    ot.append(proj_name)
    result = classifier.predict_proba(st, 5)
    records = []
    reg = '\d+'
    for record in result[0]:
        industryid = '0'
        print(record)
        try:
            industryid = re.match(reg, record[0]).group()
        except:
            industryid = '0'

        records.append({'industry': record[0][len(industryid):], 'accuracy ': record[1], 'industryid': str(industryid)})
    return records

# train_model()
# print(predict_model('红庙小学'))
