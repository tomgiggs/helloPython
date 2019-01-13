#encoding=utf8
import os.path
import numpy as np
import pandas
import matplotlib.pyplot as plt
import seaborn as sns
dataset_path = "E:\data\dataset"
pandas.set_option('display.max_rows',500)
pandas.set_option('display.max_columns',500)
pandas.set_option('display.width',1000)

source = pandas.read_csv(os.path.join(dataset_path,"countries_of_the_world.csv"),sep=",",nrows=300)
print(source.head())
pie_column = 'Population'
plt.figure(figsize=(6,6)) #指定画布大小
# x = source[pie_column].value_counts().reset_index()
x = source[['Country','Population']]
x.columns = ['Country','Population']
print(x.head())
x.sort_values(by='Population',ascending= False,axis=0,inplace=True)
top10 = x.head(10)
others = pandas.DataFrame({'Country':["others"],'Population':[x.loc[11:].sum()[1]]})
# others = x.loc[11:].sum()
# others = others.reset_index().T
# others.iat[1,0] = "other"
print(others)
# others.columns = ['Country','Population']
# print(others)
# print(top10)
rank_data = pandas.concat([top10,others],ignore_index=True)
print(rank_data)


# ax = plt.subplot(111) #绘制子图
plt.ion()
plt.pie(x = rank_data[pie_column], labels= rank_data['Country'],autopct= '%1.1f%%')
plt.legend(loc='upper right')
# ax.legend(bbox_to_anchor=(1.3, 1))
plt.title(pie_column+" pie photo")
# plt.show()
plt.pause(15) #图片一闪而过的解决方法,手动关闭图片
plt.close()

