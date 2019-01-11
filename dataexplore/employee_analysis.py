#encoding=utf8
import os.path
import numpy as np
import pandas
import matplotlib.pyplot as plt
import seaborn as sns
dataset_path = "E:\data\dataset"
pandas.set_option('display.height',1000)
pandas.set_option('display.max_rows',500)
pandas.set_option('display.max_columns',500)
pandas.set_option('display.width',1000)

source = pandas.read_csv(os.path.join(dataset_path,"employee_reviews.csv"),sep="\t",nrows=2000)
print(source.head())
source.drop(['summary','job-title','cons','pros','advice-to-mgmt','link'], axis=1,inplace=True)
print(source.head())
#-------------
pie_column = 'company'
plt.figure(figsize=(6,6)) #指定画布大小
x = source[pie_column].value_counts().reset_index()
ax = plt.subplot(111) #绘制子图
plt.pie(x = x[pie_column], labels= x['index'],autopct= '%1.1f%%')
plt.legend(loc='upper right')
ax.legend(bbox_to_anchor=(1.3, 1))
plt.title(pie_column+" pie photo")
plt.show()

#-------------------
#查看评论长度与有用数的关系
source['pros']= source['pros'].astype('str')
source["review_lens"] =source.apply(lambda  x:len(x['pros']),axis=1)
print(source["review_lens"] )
grouped = source.groupby(source['helpful-count'])['review_lens'].mean()
print(grouped)
result = grouped.reset_index()
result.sort_values(by="review_lens",ascending= True,axis=0,inplace=True)
plt.figure(figsize=(10,7))
plt.plot(result['review_lens'],result['helpful-count'])
plt.show()
#----------------------------
#查看雇员组成
plt.figure(figsize=(6,6)) #指定画布大小
x = source['job-title'].value_counts().reset_index().head(10)
ax = plt.subplot(111) #绘制子图
plt.pie(x = x['job-title'], labels= x['index'],autopct= '%1.1f%%')
plt.legend(loc='upper right')
ax.legend(bbox_to_anchor=(1.3, 1))
plt.title("job-title pie photo")
plt.show()
#----------------
#调整后再查看
plt.figure(figsize=(6,6)) #指定画布大小
x = source[source['jobname']!=' Anonymous Employee']['jobname'].value_counts().reset_index().head(10)
ax = plt.subplot(111) #绘制子图
plt.pie(x = x['jobname'], labels= x['index'],autopct= '%1.1f%%')
plt.legend(loc='upper right')
ax.legend(bbox_to_anchor=(1.3, 1))
plt.title("jobname pie photo")
plt.show()
#------------------------------
#看看哪家公司雇员给的评分最高
companyrate = source.groupby(source['company'])['overall-ratings'].mean()
print(companyrate)
#------------------
#看看各家公司给自己公司评价的关键词是什么
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
bg_image = plt.imread(r'E:\data\C360_2017-03-09-22-51-13-165.jpg')
stopwords = STOPWORDS.copy()
wc = WordCloud(width=700, height=768, background_color='white', mask=bg_image,
               stopwords=stopwords, max_font_size=400, random_state=50)
reviews = source[source['company']=='google']['pros'].tolist()
wc.generate_from_text(" ".join(reviews))
plt.imshow(wc)
plt.title("employee review wordcloud", fontsize=15)
plt.axis('off')
plt.show()
#-------------------------------
#看看各家公司的综合得分情况
source.replace("none",'0',inplace=True)
source['overall-ratings']= source['overall-ratings'].astype('float')
source['work-balance-stars']= source['work-balance-stars'].astype('float')
source['culture-values-stars']= source['culture-values-stars'].astype('float')
source['carrer-opportunities-stars']= source['carrer-opportunities-stars'].astype('float')
source['comp-benefit-stars']= source['comp-benefit-stars'].astype('float')
source['senior-mangemnet-stars']= source['senior-mangemnet-stars'].astype('float')

source["total_star"] =source.apply(lambda  x:x['senior-mangemnet-stars']+x['comp-benefit-stars']
                                   +x['carrer-opportunities-stars']+x['culture-values-stars']
                                   +x['work-balance-stars']+x['overall-ratings'],axis=1)
totalrate = source.groupby(source['company'])['total_star'].mean()
print(totalrate)
#------------------------------





