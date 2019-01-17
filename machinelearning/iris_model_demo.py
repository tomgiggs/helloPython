# encoding=utf8
import pickle
from sklearn.externals import joblib
from sklearn import datasets
import pandas
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.datasets import load_boston
iris_data = load_iris()
# np.savetxt('iris_data.csv',iris_data.data,delimiter=',')
# np.savetxt('iris_target.csv',iris_data.target,delimiter=',')
# iris_data = np.loadtxt('iris_data.csv',delimiter=',')


print('----------------iris data info ------------------')
print(iris_data.keys()) # ['target', 'DESCR', 'target_names', 'feature_names', 'data', 'filename']
print(iris_data.target_names) #['setosa' 'versicolor' 'virginica']
print(iris_data.feature_names) # ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
n_samples, n_features = iris_data.data.shape   #150*4
print(iris_data.data[0]) # [ 5.1  3.5  1.4  0.2]
print('Number of samples:', n_samples)
print('Number of features:', n_features)


from sklearn.model_selection import train_test_split
train_X, test_X, train_y, test_y = train_test_split(iris_data.data, iris_data.target,
                                                    train_size=0.8,
                                                    test_size=0.2,
                                                    random_state=50)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB

print('-------------knn model ----------------')
knn_clf = KNeighborsClassifier().fit(train_X, train_y)
pred_y01 = knn_clf.predict(test_X)
print(pred_y01)
print(test_y)
print('model score is：',knn_clf.score(test_X, test_y))
print('-------------svm model ----------------')
svm_clf = SVC( C=0.5)
svm_clf.fit(train_X,train_y)
pred_y02 = svm_clf.predict(test_X)
print(pred_y02)
print(test_y)
print('model score is：',svm_clf.score(test_X, test_y))
print('--------logisticRegression---------')
lr_clf = LogisticRegression(solver='lbfgs',multi_class='auto')
lr_clf.fit(train_X,train_y)
pred_y03 = lr_clf.predict(test_X)
print(pred_y03)
print(test_y)
print('model score is：',lr_clf.score(test_X, test_y))
print('----------decision tree ---------------')
dtc_clf = DecisionTreeClassifier()
dtc_clf.fit(train_X,train_y)
pred_y04=dtc_clf.predict(test_X)
print(test_y)
print(pred_y04)
print('model score is：',dtc_clf.score(test_X, test_y))
'''
从结果上来看，好多算法都可以做这个计算，预测结果准确率都超过0.9 ，其中logisticRegression和DecisionTree 效果最好,达到了0.967
'''


