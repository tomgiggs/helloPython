# encoding=utf8
'''
脸部识别Keras样例，参考自：https://www.cnblogs.com/neo-T/p/6477378.html
这个例子算是比较简单的样例，使用的是Keras来构建网络，比TensorFlow简单多了，TensorFlow的入门门槛还是很高的，初学者还是使用Keras来构建网络比较好
训练发现gpu没有被使用，pip list发现安装了两个版本的tensorflow，tensorflow-gpu,卸载掉tensorflow只保留gpu版本的试看看，如果还不行就卸载掉tensorflow，tensorflow-gpu，keras然后重新安装后面两个。
'''
import os
import traceback
import cv2
import random
from PIL import Image
import numpy as np
# from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.models import load_model
from keras import backend as K

model_path = r"D:\toolkit\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(model_path)
src_path = r'E:\dataset\CASIA-WebFace\CASIA-WebFace'
output_path = '../photo/avatar/'
head_model_path = './head_regn.h5'

def photo_cvt(path):
    dirs = os.listdir(path)
    for d in dirs:
        if not os.path.exists(os.path.join(output_path, d)):
            os.makedirs(os.path.join(output_path, d))
        for f in os.listdir(os.path.join(path, d)):
            try:
                raw_img = cv2.imread(os.path.join(path, d, f))
                gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 2, 5)
                for (x, y, w, h) in faces:
                    raw_img = cv2.rectangle(raw_img, (x, y), (x + w, y + h), (255, 0, 0), 0)
                    raw_img = raw_img[x:x + w, y:y + h]  # 使用数组方式截图，下面再次进行图像缩放减少像素大小
                    # resize_img = cv2.resize(raw_img, (60, 60), interpolation=cv2.INTER_CUBIC)
                    resize_img = cv2.resize(raw_img, (64, 64),
                                            interpolation=cv2.INTER_CUBIC)  # 报错：-215:Assertion failed  !ssize.empty，网上说是路径不对，莫名其妙啊
                    # cv2.imshow('find_head', raw_img)

                    cv2.imwrite(os.path.join(output_path, d, f), resize_img)
            except:
                traceback.print_exc()
            # return

def photo_cvt2(path):
    dirs = os.listdir(path)
    for d in dirs:
        for f in os.listdir(os.path.join(path, d)):
            try:
                raw_img = cv2.imread(os.path.join(path, d, f))
                resize_img = cv2.resize(raw_img, (64, 64),
                                        interpolation=cv2.INTER_CUBIC)  # 报错：-215:Assertion failed  !ssize.empty，网上说是路径不对，莫名其妙啊
                cv2.imwrite(os.path.join(output_path, d, f), resize_img)
            except:
                traceback.print_exc()

def load_dataset(path):
    dirs = os.listdir(path)
    images = []
    labels = []
    for d in dirs:
        for f in os.listdir(os.path.join(path, d)):
            raw_img = cv2.imread(os.path.join(path, d, f))
            images.append(raw_img)
            labels.append(d)
    return np.array(images), np.array(labels),len(dirs)

def reshape_dataset(dataset_path, img_width, img_hight, img_channel, nb_classes=2):
    images, labels,classes = load_dataset(dataset_path)
    train_images, test_images, train_labels, test_labels = train_test_split(images, labels, train_size=0.8, test_size=0.2, random_state=50)

    if K.image_dim_ordering() == 'th':
        # train_images = train_images.reshape(train_images.shape[0], img_channel, img_hight, img_width)
        # test_images = test_images.reshape(test_images.shape[0], img_channel, img_hight, img_width)
        input_shape = (img_channel, img_hight, img_width)
    else:
        # train_images = train_images.reshape(train_images.shape[0], img_hight, img_width, img_channel) #报错cannot reshape array of size 16 into shape (16,64,64,3)，reshape不了是为什么呢。。。
        # test_images = test_images.reshape(test_images.shape[0], img_hight, img_width, img_channel)
        input_shape = (img_hight, img_width, img_channel)
        print(train_images.shape[0], 'train samples')
        print(test_images.shape[0], 'test samples')

        # 我们的模型使用categorical_crossentropy作为损失函数，因此需要根据类别数量nb_classes将类别标签进行one-hot编码使其向量化，经过转化后标签数据变为二维，
        # 遇到编码失败了，这个编码要求每个元素有一个唯一的编码，如果中间有跳过那就需要以最大的元素为编码数量
        train_labels = np_utils.to_categorical(train_labels, 160) #报错：ValueError: setting an array element with a sequence.前后数组维数不一致,IndexError: index 117 is out of bounds for axis 1 with size 21
        test_labels = np_utils.to_categorical(test_labels, 160)

        # 像素数据浮点化以便归一化
        train_images = train_images.astype('float32')
        test_images = test_images.astype('float32')

        # 将其归一化,图像的各像素值归一化到0~1区间
        train_images /= 255
        test_images /= 255
        # return [input_shape, train_images, test_images, train_labels, test_labels]
        return {
            "input_shape":input_shape,
            "train_images":train_images,
            "test_images":test_images,
            "train_labels":train_labels,
            "test_labels":test_labels
        }

def build_model(dataset):
    model = Sequential()
    model.add(Convolution2D(32, (3, 3), border_mode='same', input_shape=dataset["input_shape"]))
    model.add(Activation('relu'))
    model.add(Convolution2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))#dropout层，每次随机禁用一部分的神经元，通过这样来保证神经元的独立，避免过拟合
    model.add(Convolution2D(64, (3, 3), border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(160))#全连接层，输出层维度，跟上面one_hot编码的维度对应
    model.add(Activation('softmax'))
    model.summary()#打印模型信息
    return model
'''
模型运行遇到的问题：
Could not find 'cudart64_100.dll' ，已经安装对的版本也还是一直报错，最后打开cmd执行发现是可以的，重启pycharm就可以了，这个是真坑。。
tensorflow-gpu版本要求比较多，必须在系统中安装以下 NVIDIA® 软件：
NVIDIA® GPU 驱动程序 - CUDA 10.0 需要 410.x 或更高版本。
CUDA® 工具包 - TensorFlow 支持 CUDA 10.0（TensorFlow 1.13.0 及更高版本）
CUDA 工具包附带的 CUPTI。
cuDNN SDK（7.4.1 及更高版本）
（可选）TensorRT 5.0，可缩短在某些模型上进行推断的延迟并提高吞吐量。
最坑的就是我安装了cudas10.1，然而目前tensorflow只支持cuda10.0.。。。
Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
'''

def train(batch_size=20, nb_epoch=10, data_augmentation=True):
    head_model_path = './head_regn.h5'
    dataset_path = r'../photo/avatar'
    dataset = reshape_dataset(dataset_path, 64, 64, 3)
    model = build_model(dataset)
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)  # 采用SGD+momentum的优化器进行训练，首先生成一个优化器对象
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])  # 完成实际的模型配置工作
    if not data_augmentation:
        model.fit(dataset["train_images"], dataset["train_labels"], batch_size=batch_size, nb_epoch=nb_epoch,
                  validation_data=(dataset['test_images'], dataset["train_labels"]), shuffle=True)
    else:
        # 定义数据生成器用于数据提升，其返回一个生成器对象datagen，datagen每被调用一次其生成一组数据（顺序生成），节省内存，其实就是python的数据生成器
        datagen = ImageDataGenerator(
            featurewise_center=False,  # 是否使输入数据去中心化（均值为0），
            samplewise_center=False,  # 是否使输入数据的每个样本均值为0
            featurewise_std_normalization=False,  # 是否数据标准化（输入数据除以数据集的标准差）
            samplewise_std_normalization=False,  # 是否将每个样本数据除以自身的标准差
            zca_whitening=False,  # 是否对输入数据施以ZCA白化
            rotation_range=20,  # 数据提升时图片随机转动的角度(范围为0～180)
            width_shift_range=0.2,  # 数据提升时图片水平偏移的幅度（单位为图片宽度的占比，0~1之间的浮点数）
            height_shift_range=0.2,  # 同上，只不过这里是垂直
            horizontal_flip=True,  # 是否进行随机水平翻转
            vertical_flip=False)  # 是否进行随机垂直翻转

        # 计算整个训练样本集的数量以用于特征值归一化、ZCA白化等处理
        datagen.fit(dataset["train_images"])
        # 利用生成器开始训练模型
        model.fit_generator(datagen.flow(dataset["train_images"], dataset["train_labels"], batch_size=batch_size),
                            samples_per_epoch=dataset["train_images"].shape[0], nb_epoch=nb_epoch,
                            validation_data=(dataset["train_images"], dataset["train_labels"]))
        model.save(head_model_path)

def load_h5_model():
    dataset_path = r'../photo/avatar'
    images, labels,classes = load_dataset(dataset_path)#返回的images是一个list<array>格式的，并不是numpy数组，为什么呢？
    train_images, test_images, train_labels, test_labels = train_test_split(images, labels, train_size=0.8,
                                                                            test_size=0.2, random_state=50)
    model = load_model(head_model_path)
    # model.evaluate(test_images, test_labels, verbose=160)
    predict_test = model.predict_classes(test_images).astype('int')
    i = 0
    right = 0
    for predict in predict_test:
        if int(test_labels[i])==predict:
            right +=1
    # print(predict_test)
    print(len(test_labels),right)
    pass
# photo_cvt2( r'../photo/avatar')
# train()
load_h5_model()