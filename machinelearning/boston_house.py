#encoding=utf8
print(__doc__)
from sklearn import datasets
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
binarizer = preprocessing.Binarizer().fit()
# lr = linear_model.LinearRegression()
# boston = datasets.load_boston()
# y = boston.target

#对数据进行分组
# from sklearn.model_selection import LeavePOut
# lpo = LeavePOut(p=2)
# for tran,test in lpo.split(boston.data):
#     print(tran,test)


# predicted = cross_val_predict(lr, boston.data, y, cv=10)
#
# fig, ax = plt.subplots()
# ax.scatter(y, predicted, edgecolors=(0, 0, 0))
# ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
# ax.set_xlabel('Measured')
# ax.set_ylabel('Predicted')
# plt.show()