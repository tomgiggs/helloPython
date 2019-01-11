#encoding=utf8
import pandas
import numpy
import time
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

source = pandas.read_csv(r'E:\data\dataset\amazon_alexa.tsv',sep="\t",
                         nrows=5000
                         )
# print(source.head())
source['date'] = pandas.to_datetime(source['date'], errors='coerce')
# print(source['date'].dt.weekday_name)
#----------------------------------------
#绘制评论词云
bg_image = plt.imread(r'E:\data\C360_2017-03-09-22-51-13-165.jpg')
stopwords = STOPWORDS.copy()
stopwords.add("love")
stopwords.add("Alexa")
stopwords.add("echo")
stopwords.add("use")
wc = WordCloud(width=700, height=768, background_color='white', mask=bg_image,
               stopwords=stopwords, max_font_size=400, random_state=50)
reviews = source['verified_reviews'].tolist()
wc.generate_from_text(" ".join(reviews))
plt.imshow(wc)
plt.title("Alexa reviews wordcloud", fontsize=30)
plt.axis('off')
plt.show()
#----------------------------------------
#绘制评分饼图
# plt.figure(figsize=(6,6)) #指定画布大小
# x = source['rating'].value_counts().reset_index()
# ax = plt.subplot(111) #绘制子图
# plt.pie(x = x['rating'], labels= x['index'],autopct= '%1.1f%%')
# plt.legend(loc='upper right')
# ax.legend(bbox_to_anchor=(1.3, 1))
# plt.title("Alexa rating pie photo")
# plt.show()
#----------------------------------------
# #查看评论量虽时间的变化趋势
# date_info = source['date'].value_counts().reset_index() #加reset_index将series变为dataframe
# # print(date_info)
# date_info.columns = ['date','count']
# # print(date_info)
# data_rank = date_info.sort_values(by="date",ascending= True,axis=0,
#  # inplace = True #是否替换原来的值，否的话会返回一个排序后的dataframe
# )
# plt.figure(figsize=(10,7))
# plt.plot(data_rank['date'], data_rank['count'])
# plt.show()
#----------------------------------------




