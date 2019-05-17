#encoding=utf8
'''
参考官方cifar10代码实现
'''
import os
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import mnist
source_fold = r'E:\dataset\tf_data\mnist_test'

def read_data(fileNameQue=None):
    class MnistRecord(object):
        pass

    result = MnistRecord()

    #下面的做法不适合在读取文件时打散文件，不然会出现标签对不上的问题
    train_photos = []
    label = []
    for t in range(10):
        label.append(str(t))
        file_list = os.listdir(source_fold + os.sep + str(t))
        for f in file_list:
            train_photos.append(os.path.join(source_fold,f))
    filename_queue = tf.train.string_input_producer(train_photos) #这个如何处理标签呢
    # imagepath, label = tf.train.slice_input_producer([train_photos, label], shuffle=True)
    # reader = tf.FixedLengthRecordReader(record_bytes=3076)
    # reader = tf.TextLineReader(skip_header_lines=1)
    # image_value = tf.read_file('test.jpg')
    # image_raw = tf.gfile.FastGFile('test.jpg', 'rb').read()
    reader = tf.WholeFileReader()
    key, value = reader.read(filename_queue)
    images = tf.decode_raw(value, tf.uint8) # 解码
    result.labels = tf.convert_to_tensor(label) #将列表(numpy)转换为tensor
    depth_major = tf.reshape(images,[3, 28, 28])
    uint8image = tf.transpose(depth_major, [1, 2, 0])
    result.reshaped_image = tf.cast(uint8image, tf.float32) # 转换数据类型，这个只能用于tensor和tensor的转换
    return result

# read_data()

def shuffle_data(image,label,batch_size=2000,thread_num=1,min_queue_examples=1000):
    # images, label_batch = tf.train.shuffle_batch(
    #     [images, labels],
    #     batch_size=batch_size,
    #     num_threads=thread_num,
    #     capacity=5 * batch_size,min_after_dequeue=2*batch_size)
    images, label_batch = tf.train.shuffle_batch(
        [image, label],
        batch_size=batch_size,
        num_threads=thread_num,
        capacity=min_queue_examples + 3 * batch_size,
        min_after_dequeue=min_queue_examples)
    tf.summary.image('images', images)
    return images, tf.reshape(label_batch, [batch_size*10]) #Cannot reshape a tensor with 2000 elements to shape [200] (200 elements) for 'Reshape_1'


def train():
    input_data = read_data()
    imgs,labels = shuffle_data(input_data.reshaped_image,input_data.labels,batch_size=128)
    x = tf.placeholder(tf.float32, [None, 784]) # 使用占位符声明后面变量会存储的数据类型及维度信息等（因为底层用C实现，
    # 所以需要类型信息，还有维度信息（创建多维数组要用到））
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.matmul(x, W) + b #定义算法（目标函数）
    y_ = tf.placeholder(tf.int64, [None]) #声明标记数据的维度
    cross_entropy = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=y) #定义计算损失函数
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)# 计算损失函数的具体方式
    sess = tf.InteractiveSession()#创建会话
    tf.global_variables_initializer().run() #启动图，开始计算
    threads = tf.train.start_queue_runners(sess=sess) #开始读取文件
    saver = tf.train.Saver(max_to_keep=1) #模型保存器
    for s in range(30):
        batch_xs, batch_ys = tf.train.batch([imgs],200),tf.train.batch([labels],200) #获取训练数据,，第一个参数需要是列表，不然会报错无法迭代,
        # 这个能保证数据与标签对应吗
        # TypeError: `Tensor` objects are not iterable when eager execution is not enabled. To iterate over this tensor use `tf.map_fn`.
        # sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys}) #开始训练,raise TypeError('The value of a feed cannot be a tf.Tensor object. '
        sess.run(train_step, feed_dict={x: batch_xs.eval(session=sess), y_: batch_ys.eval(session=sess)})
        # TypeError: input must be a dictionary,使用batch_xs.eval(session=sess)才行,这样做虽然可以运行的，但是效率实在是太低了，慢的要死
        if s%500==0:
            saver.save(sess, 'ckpt/mnist.tfmodel', global_step=s+1) #保存模型

    correct_prediction = tf.equal(tf.argmax(y, 1), y_) # 计算模型预测值与实际值的差距
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) #将每次预测结果转化为数值，然后求平均值
    print(sess.run(
        accuracy, feed_dict={
            x: mnist.test.images,
            y_: mnist.test.labels
        })) # 计算预测准确度

if __name__=='__main__':
    train()

