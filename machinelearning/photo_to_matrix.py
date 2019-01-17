# encoding=utf8
import pickle
import os
import glob  #查找符合特定规则的文件路径名
# import os.path
import numpy
import pandas
import cv2
# numpy.set_printoptions(threshold='nan')  # 取消输出折叠
# numpy.set_printoptions(threshold=numpy.nan)
# source_folder = r'E:\data\dataset\tf_data\mnist_train\0'
# pictures = os.listdir(source_folder)
#
# img = cv2.imread(os.path.join(source_folder,pictures[0]))
# img2 = cv2.imread(os.path.join(source_folder,pictures[1]))
# print(img.shape) # (28, 28, 3) 3是每个坐标（像素点）有三个取值（三个色彩层叠加）
# print(cv2.threshold(img,20,255,cv2.THRESH_BINARY)) #转化为二值图，阈值为threahold，小于阈值设为0，大于阈值设为255
# print(cv2.split(img)[0].shape)  # (28, 28)剥离成单通道图像合并的话使用merge函数
#
# photo_array = numpy.array(img)
# new_array = numpy.stack((photo_array,img2))
# print(new_array.shape) # (2, 28, 28, 3)
# print(numpy.hstack((photo_array,img2)).shape)# (28, 56, 3)

# matrix = numpy.array(img)
matrix = []
target = []
for i in range(9):
    raw_fold = r'E:\data\dataset\tf_data\mnist_train' + '\\' + str(i)
    for photo in os.listdir(raw_fold)[:15]:
        target.append(i)
        img = cv2.imread(os.path.join(raw_fold, photo),0) #读取蓝色图层，不加后面这个0的话是读取所有图层
        # cv2.resize(img, (25, 25), interpolation=cv2.INTER_AREA)
        # matrix.append(img.tolist())
        # matrix.append(img.reshape(784).tolist())#手动将数据变成二维结构
np_matrix = numpy.array(matrix)
print(np_matrix.shape) #(135, 28, 28)
# print(np_matrix)
from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(np_matrix, target,
                                                    train_size=0.8,
                                                    test_size=0.2,
                                                    random_state=50)
from sklearn.svm import SVC
svm_clf = SVC(verbose=0, kernel='poly', degree=3)
svm_clf.fit(train_x,train_y) # 报错：ValueError: Found array with dim 3.搜索后发现是因为sklearn只支持输入二维数据
#  Estimator expected <= 2,scikit-learn expects 2d num arrays for the training dataset for a fit function.
# The dataset you are passing in is a 3d array you need to reshape the array into a 2d.
pred_y02 = svm_clf.predict(test_x)
print(pred_y02)
print(test_y)
print('model score is:',svm_clf.score(test_x, test_y)) # 0.62962962962962965,很低，因为拍平之后丢失了像素间的有价值的联系（图像是块状相连的）

