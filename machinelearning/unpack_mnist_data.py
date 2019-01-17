#encoding=utf8
import numpy as np
import struct
from PIL import Image
import os
source_dir = r'E:\data\dataset\tf_data'

def unpack_data(data_file=''):
    # It's 47040016B, but we should set to 47040000B
    # train_size is : 47040016,test size is :7840016
    data_file_size = os.path.getsize(data_file)
    data_file_size = str(data_file_size - 16) + 'B'
    data_buf = open(data_file, 'rb').read()
    magic, numImages, numRows, numColumns = struct.unpack_from(
        '>IIII', data_buf, 0)
    datas = struct.unpack_from(
        '>' + data_file_size, data_buf, struct.calcsize('>IIII'))
    datas = np.array(datas).astype(np.uint8).reshape(
        numImages, 1, numRows, numColumns)
    # print(datas.shape) # (60000, 1, 28, 28)
    # print(len(datas)) # 60000
    return datas

def get_label(path=''):
    # It's 60008B, but we should set to 60000B
    # train_size is : 60008,test size is :10008
    label_file_size = os.path.getsize(path)
    label_file_size = str(label_file_size - 8) + 'B'
    label_buf = open(path, 'rb').read()
    magic, numLabels = struct.unpack_from('>II', label_buf, 0)
    labels = struct.unpack_from(
        '>' + label_file_size, label_buf, struct.calcsize('>II'))
    labels = np.array(labels).astype(np.int64)
    print(labels.shape) #(60000,)
    return labels


def write_file(datas,labels,datas_root=''):

    if not os.path.exists(datas_root):
        os.mkdir(datas_root)
    for i in range(10):
        file_name = os.path.join(datas_root , str(i))
        if not os.path.exists(file_name):
            os.mkdir(file_name)
    label_num = len(labels)
    for t in range(label_num):
        # img = Image.fromarray(datas[t, 0, 0:28, 0:28])
        img = Image.fromarray(datas[t,0])
        label = labels[t]
        file_name = datas_root + os.sep + str(label) + os.sep + \
                    'mnist_train_' + '%05d'%t + '.png'
        img.save(file_name)


def unpack_train():
    data_root =  os.path.join(source_dir,'mnist_train') #需要修改的路径
    train_data_file = os.path.join(source_dir,'train-images.idx3-ubyte')#需要修改的路径
    train_label_path = os.path.join(source_dir,'train-labels.idx1-ubyte')#需要修改的路径
    train_data = unpack_data(train_data_file)
    # print(train_data[1, 0, 0:28, 0:28].shape) #(28, 28),方括号中逗号分隔符是取元素，每个逗号都是往下取下一个元素，冒号是切片
    # print(train_data[1]) # (1, 28, 28)
    # print(train_data[1, 0, 7, 8]) # 0
    # img = Image.fromarray(train_data[1, 0, 0:28, 0:28])
    # img.save("one_photo.png")
    # img.show()
    train_label = get_label(train_label_path)
    write_file(train_data,train_label,data_root)
def unpack_test():
    data_root =  os.path.join(source_dir,'mnist_test') #需要修改的路径
    train_data_file = os.path.join(source_dir,' t10k-images.idx3-ubyte')#需要修改的路径
    train_label_path = os.path.join(source_dir,'t10k-labels.idx1-ubyte')#需要修改的路径
    train_data = unpack_data(train_data_file)
    train_label = get_label(train_label_path)
    write_file(train_data,train_label,data_root)

def main():
    unpack_train()
    unpack_test()

main()
