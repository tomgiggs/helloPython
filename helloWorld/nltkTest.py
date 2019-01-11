import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import matplotlib.pylab as pl
import sys
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread
def cut_sentence():
    raw_str = open(r'D:\nltk_data\corpora\gutenberg\austen-persuasion.txt','r').read()
    #raw_str = ' Professional -Self Healing Cutting Mat is a cut above the rest!  :) Alvin Professional -Self Alvin Professional -Self'
    cutted = WordPunctTokenizer().tokenize(raw_str)
    # w = []
    # for x in cutted:
    #     if x not in stopwords.words('english'):
    #         w.append(x)
    #filtered = [w  for w in cutted if (w not in stopwords.words('english')]
    #print(w)
    #print(cutted)
    col = FreqDist(cutted)
    #col.plot()
    col.tabulate()
    # print(col.max())
    # print(col.N())
    # print(col.B())
    # # tags = nltk.tag._get_tagger('eng')
    # # print(tags.tag(col))
    # print(nltk.pos_tag(col))

#cut_sentence()

def wordCloud():
    raw_str = open(r'D:\nltk_data\corpora\gutenberg\austen-persuasion.txt','r').read()
    cutted = WordPunctTokenizer().tokenize(raw_str)
    background = plt.imread(r'd:\data\bg_img2.jpg')
    seg_space = ' '.join(cutted)
    fwc = WordCloud( max_words=700, background_color='white', mask=background, max_font_size=100,font_step=1,min_font_size=15).generate(seg_space)
    imagecolor = ImageColorGenerator(background)
    plt.imshow(fwc.recolor(color_func=imagecolor))
    plt.axis("off")
    plt.show()

wordCloud()
# nltk.download()
