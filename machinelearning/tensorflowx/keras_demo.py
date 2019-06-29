'''
这是一个Keras的样例代码，参考了博客：https://blog.csdn.net/cymy001/article/details/78647640
试用与数据量不是特别大的情况，因为使用了很多numpy，sklearn对数据的操作，在数据量大的时候可能会因为在c++与Python数据格式之间频繁转换而造成严重的性能损失
'''
import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from keras.layers import Activation, Conv2D, MaxPooling2D, Flatten, Dropout
import os
from PIL import Image
import numpy
from sklearn.model_selection import train_test_split  # 用来切分数据

# 读取文件夹里面的图片，这个数据集是从mnist里面解压还原出来的，如果这个跑通过了，后面使用自定义数据集就没什么大的问题了，
# 不过自定义数据集需要进行预处理，将图片尺寸进行统一，转换色彩空间，进行适当的裁剪，避免尺寸不一样造成错误和图片太大造成计算量庞大

img_path = r'E:\dataset\tf_data\mnist_test'  # 数据目录，以目录为标签，存有0-9对应的图片
images = []
labels = []
num = 0
for label in os.listdir(img_path):
    for img in os.listdir(os.sep.join([img_path, label])):
        img_body = Image.open(os.sep.join([img_path, label, img]))  # 读取图片
        images.append(numpy.array(img_body))  # 转换成矩阵
        labels.append(label)
        num += 1
        if num > 50:  # 每次改变训练输入数据的大小，观察模型准确度的改变
            num = 0
            break

images = numpy.array(images)  # 将列表再次转换成numpy结构，不然后面打印不出shape
labels = numpy.array(labels)
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.3)  # 使用sklearn的 数据集切分函数进行数据切分

# (x_train,y_train),(x_test,y_test) = mnist.load_data()#加载模型自带的数据，这里不使用自定义数据
# print('x_shape:', x_train.shape)
# print('y_shape:', y_train.shape)
# x_shape: (357, 28, 28)
# y_shape: (357,)

# #------------模型1---------
# x_train = x_train.reshape(x_train.shape[0], -1) / 255.0 #这个是给拍平了吗，那不就丢失了很多信息了？图像是通过和周围的像素点一起计算的，这样有问题吧
# x_test = x_test.reshape(x_test.shape[0], -1) / 255.0
# #再次查看模型维度
# print('x_shape:', x_train.shape)
# print('y_shape:', y_train.shape)
# # x_shape: (357, 784)
# # y_shape: (357,)
# #我要怎么知道我应该讲数据变换成什么维度的数据呢？我怎么知道我应该定义一个什么样的模型呢？
# # 转换标签one-hot格式，因为一个很重要的原因在于计算loss时的问题。loss一般用距离来表示，如果用1~10来表示，那么1和2的距离时1，而1和5的距离时4，但是按道理1和2、1和5的距离应该一样。one-hot编码可以解决类别型数据的离散值问题
# y_train = np_utils.to_categorical(y_train, num_classes=10)
# y_test = np_utils.to_categorical(y_test, num_classes=10)
# # 创建模型，输入784个神经元，输出10个神经元,注意参数是一个列表，
# model = Sequential([Dense(units=10, input_dim=784, bias_initializer='one', activation='softmax')])
# sgd = SGD(lr=0.2)
# model.compile(optimizer=sgd, loss='mse', metrics=['accuracy'], )
# model.fit(x_train, y_train, batch_size=64, epochs=5)
# loss, accuracy = model.evaluate(x_test, y_test)
# print('test loss:', loss)
# print('accuracy', accuracy)
# model.save('model2.h5')
# #---------模型2-----------

# 不经过下面这两句代码处理的话会报错：ValueError: Error when checking input: expected dense_1_input to have 2 dimensions, but got array with shape (4204, 28, 28)

# model.add 可以继续往模型添加网络层
# y_train = np_utils.to_categorical(y_train, num_classes=10)
# y_test = np_utils.to_categorical(y_test, num_classes=10)

#构建模型
model = Sequential()
model.add(Dense(units=10, input_dim=784,bias_initializer='one', activation='softmax'))#添加一个2D层，Dense 2D层
#定义一个优化器
sgd = SGD(lr=0.2)
#编译模型
model.compile(optimizer=sgd, loss='mse', metrics=['accuracy'], )
#开始训练
model.fit(x_train, y_train, batch_size=64, epochs=5)
#模型评估
loss, accuracy = model.evaluate(x_test, y_test)
print('test loss:', loss)
print('accuracy', accuracy)
#保存模型
model.save('model2.h5')



