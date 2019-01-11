#encoding=utf8
# from https://www.kaggle.com/hashbanger/google-simplanalysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pylab import rcParams
# pandas在打开Excel，CSV和读取数据库并做一些统计及可视化方法是非常强大的，使用pandas来探索数据是成为数据分析与挖掘工程师必不可少的技能。
#下面尝试把pandas当成数据库来做SQL能做的事情，同时绘制一些图
df = pd.read_csv("E:\data\dataset\googleplaystore.csv") #读取数据，pandas还可以把数据写入到数据库和转变成json，简直神器。
print(df.describe().T) # 描述数据的基本特征
#print(df['Category'].unique)
print(len(df['Genres'].value_counts()))
# 这行代码就可以查看各列不同值出现的次数，相当于SQL中的group by
x = df['Genres'].value_counts().reset_index().head(50)
print(type(x))
plt.figure(figsize=(12,12)) #指定画布大小
ax = plt.subplot(111) #绘制子图
plt.pie(x = x['Genres'], labels= x['index'],autopct= '%1.1f%%') #画一个饼图
plt.legend(loc='upper right') # 添加图例（颜色含义说明，默认在右上角，如果要在其他位置，需要穿一个字符串参数，没错，就是字符串参数。。。）
ax.legend(bbox_to_anchor=(1.4, 1))
plt.show() #把图显示出来，真的是画个图秒秒钟的事情，不必Excel差多少
select_data = df[df['Category']=='FAMILY'] #这种就跟SQL里面select * from xxx where Category='' 一样，下面head(5)就跟limit或者rownum<5一样
print(select_data.head(5))
#再画个直方图？
df.dropna(how = 'any', inplace = True)# 删除整行为NaN的值，how控制删除条件，可选的还有any,all等
# df.fillna(0)#填充NaN值，不然绘图时会报错
plt.figure(figsize=(10,7))
#plt.hist(df['Rating'])#plt自带的图片太丑了，还是用seaborn比较好看点
sns.distplot(df['Rating'])
plt.legend(['Rating'])
plt.show()
print(np.average(df['Rating']))#看一下评分平均值
#print(df.info())#查看发现review值为字符串，需要先转换类型
df['Reviews']= df['Reviews'].astype('int')
review_count = df['Reviews'].value_counts().reset_index()['index']
# review_cunnt = pd.to_numeric(review_count.values, errors='ignore')
# #print(review_count.sort_index(ascending=False))#对索引排序，没什么用
reviews_rank = review_count.sort_values(ascending=False) #查看一下评论量排序
print(reviews_rank.head(10))
print(df.size) #查看记录总数
print(df[df['Installs'] > 1000000].sort_values(by = 'Installs', ascending = False).head(20)['App'])
#查看评论数top20应用名称,或者安装量前20的应用





