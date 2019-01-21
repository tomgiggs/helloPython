# encoding=utf8

import os
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


# copy from http://www.360doc.com/content/17/0419/15/10408243_646848256.shtml
def make_tf_record():
    cwd = r'D:\data\tf\mnist_test'
    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    writer = tf.python_io.TFRecordWriter("mnist.tfrecords")

    for index, name in enumerate(classes):
        class_path = cwd + '\\' + name + '\\'
        for img_name in os.listdir(class_path):
            img_path = class_path + img_name
            img = Image.open(img_path)
            img = img.resize((28, 28))
            img_raw = img.tobytes()
            example = tf.train.Example(features=tf.train.Features(feature={
                "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
                'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
            }))
            writer.write(example.SerializeToString())

    writer.close()


# make_tf_record()


def read_tf_record(filename):
    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw': tf.FixedLenFeature([], tf.string),
                                       })

    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [28, 28, 3])  # reshape为128*128的3通道图片
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5  # 在流中抛出img张量
    label = tf.cast(features['label'], tf.int32)  # 在流中抛出label张量
    return img, label


def release_tf_record():
    filename_queue = tf.train.string_input_producer(["dog_train.tfrecords"])
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw': tf.FixedLenFeature([], tf.string),
                                       })  # 取出包含image和label的feature对象
    image = tf.decode_raw(features['img_raw'], tf.uint8)
    image = tf.reshape(image, [128, 128, 3])
    label = tf.cast(features['label'], tf.int32)
    cwd = os.getcwd()
    with tf.Session() as sess:  # 开始一个会话
        init_op = tf.initialize_all_variables()
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        for i in range(20):
            example, l = sess.run([image, label])  # 在会话中取出image和label
            img = Image.fromarray(example, 'RGB')  # 这里Image是之前提到的
            img.save(cwd + str(i) + '_''Label_' + str(l) + '.jpg')  # 存下图片
            print(example, l)
        coord.request_stop()
        coord.join(threads)
    pass
