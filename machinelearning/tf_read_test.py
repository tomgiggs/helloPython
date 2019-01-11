#encoding=utf8
from matplotlib import pyplot as plt
import tensorflow as tf
import numpy as np
import os,sys


#read img files:
file_names = os.listdir(r'D:\data\tf\mnist_train\1')
file_name_queue = tf.train.string_input_producer(file_names,shuffle=False,num_epochs=2)

img_reader = tf.WholeFileReader()
key, image = img_reader.read(file_name_queue)
image = tf.image.decode_jpeg(image)
with tf.Session() as sess:
    # coord = tf.train.Coordinator() #协同启动的线程
    # threads = tf.train.start_queue_runners(sess=sess, coord=coord) #启动线程运行队列
    # coord.request_stop() #停止所有的线程
    # coord.join(threads)
    tf.local_variables_initializer().run()
    #怎么获取输出？
    threads = tf.train.start_queue_runners(sess=sess)
    for i in range(2):
        plt.figure
        plt.imshow(image.eval())
        plt.show()


#read one image
# img_value = tf.read_file(r'D:\data\tf\mnist_train\1\mnist_train_3.png')
# img = tf.image.decode_image(img_value,channels=3)

#gfile reader
image_raw = tf.gfile.FastGFile(r'D:\data\tf\mnist_train\1\mnist_train_3.png','rb').read()   #bytes
img = tf.image.decode_jpeg(image_raw)  #Tensor
# with tf.Session() as sess:
#     print(type(img.eval()))
#     print(img.eval().shape)
#     print(img.eval().dtype)
#     plt.imshow(img.eval())
#     plt.show()



