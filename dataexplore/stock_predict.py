#encoding=utf8
import os.path
import  prophet
from fbprophet import Prophet
import pandas
import numpy

dataset_path = "E:\data\dataset\stock_series"
# pandas.set_option('display.height',1000) #python 3 不支持这个设置
pandas.set_option('display.max_rows',500)
pandas.set_option('display.max_columns',500)
pandas.set_option('display.width',1000)
source = pandas.read_csv(os.path.join(dataset_path,"IBM_2006-01-01_to_2018-01-01.csv"),sep=",",nrows=2000)
source['ds'] = pandas.to_datetime(source['Date'], errors='coerce') #输入是一个DataFrame，必须包含这两列：ds 和 y。ds 必须是一个 date 或者 datetime。y 必须是数字，代表我们需要预测的序列的值。
source['y'] = source['High']

print(source.head())

model = Prophet()#指定节假日参数，其它参数以默认值进行训练
model.fit(source)#对过去数据进行训练
future = model.make_future_dataframe(freq='D',periods=120)#建立数据预测框架，数据粒度为天，预测步长为一年
forecast =model.predict(future)
from matplotlib import pyplot as plt
fig = model.plot(forecast)
# fig2 = model.plot_components(forecast)
plt.show()
# model.plot(forecast).show()#绘制预测效果图 这个会报错 Could not load matplotlib icon: can't use "pyimage10" as iconphoto
# model.plot_components(forecast).show()#绘制成分趋势图





