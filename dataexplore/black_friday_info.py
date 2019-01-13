#encoding=utf8
import os.path
import pandas
import numpy
import matplotlib.pyplot as plt

dataset_path = "E:\data\dataset"
pandas.set_option('display.max_rows',500)
pandas.set_option('display.max_columns',500)
pandas.set_option('display.width',1000)
source = pandas.read_csv(os.path.join(dataset_path,"BlackFriday.csv"),sep=",",nrows=5000)
print(source.head())
#--------------------
#查看购买金额前十
# source.sort_values(by='Purchase',ascending=False,inplace=True,axis=0)
# print(source.head())
#-----------------------------
#看看那个年龄段购买力最强
# age_group = source.groupby(by='Age')['Purchase']
# print(type(age_group))
# print(age_group.sum())
# print(age_group.mean())
# avg_purchase = age_group.mean().reset_index()
# plt.figure(figsize=(6,6)) #指定画布大小
# ax = plt.subplot(111) #绘制子图
# plt.pie(x = avg_purchase['Purchase'], labels= avg_purchase['Age'],autopct= '%1.1f%%')
# plt.legend(loc='upper right')
# ax.legend(bbox_to_anchor=(1.3, 1))
# plt.title("jobname pie photo")
# plt.show()
#----------------
#看看哪些商品最畅销
# item_info  = source.groupby(by='Product_ID')['Purchase']
# item_amount = item_info.sum().reset_index().sort_values(by='Purchase',ascending= False,axis=0,inplace=False)
# item_sell_num = item_info.count().reset_index().sort_values(by='Purchase',ascending= False,axis=0,inplace=False)
# item_avg_amount = item_info.mean().reset_index().sort_values(by='Purchase',ascending= False,axis=0,inplace=False)
# print(item_amount)

#-----------------------------
#看看男人还是女人购买金额更高
# age_group = source.groupby(by='Gender')['Purchase']
# print(type(age_group))
# print(age_group.sum())
# print(age_group.mean())
# # avg_purchase = age_group.mean().reset_index()
# avg_purchase = age_group.sum().reset_index()
# plt.figure(figsize=(6,6)) #指定画布大小
# ax = plt.subplot(111) #绘制子图
# plt.pie(x = avg_purchase['Purchase'], labels= avg_purchase['Gender'],autopct= '%1.1f%%')
# plt.legend(loc='upper right')
# ax.legend(bbox_to_anchor=(1.3, 1))
# plt.title("Gender pie photo")
# plt.show()
# -------------------------------
#查看城市购买份额
age_group = source.groupby(by='City_Category')['Purchase']
# print(type(age_group))
# print(age_group.sum())
# print(age_group.mean())
# avg_purchase = age_group.mean().reset_index()
# avg_purchase = age_group.sum().reset_index()
# plt.figure(figsize=(6,6)) #指定画布大小
# ax = plt.subplot(111) #绘制子图
# plt.pie(x = avg_purchase['Purchase'], labels= avg_purchase['City_Category'],autopct= '%1.1f%%')
# plt.legend(loc='upper right')
# ax.legend(bbox_to_anchor=(1.3, 1))
# plt.title("City_Category pie photo")
# plt.show()
#----------------------------------------------
#看哪些买家购买力最强
age_group = source.groupby(by='User_ID')['Purchase']
print(age_group.sum().reset_index().sort_values(by='Purchase',ascending=False,inplace=False,axis=0))
#-------------------------------------
#看看购买力最强的消费者有什么特征


