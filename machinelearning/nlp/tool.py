# encoding=utf8
import re

stopwords = {
    "eng": set([line.strip('\n') for line in open('./stop_words_en.txt', "r", encoding="utf8").readlines()]),
    "zhcn": set([line.strip('\n') for line in open('./stop_words_zhcn.txt', "r", encoding="utf8").readlines()])
}

def remove_special_char(content):
    line = re.sub("[:\.\!\/_,$%^<>*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", content)
    return line.replace("\n", " ").replace("\t", " ").replace("  ", " ")


def remove_stop_word(content, lang="eng"):
    new_content = []
    for word in content.split(' '):
        if word not in stopwords[lang]:
            new_content.append(word)
    return new_content


def clean_text(content):
    pass
