import tensorflow as tf
from tensorflow.examples.tutorials.mnist import mnist
import os
i = 0
def read_data(fileNameQue):

    reader = tf.TFRecordReader()
    key, value = reader.read(fileNameQue)
    features = tf.parse_single_example(value, features={'label': tf.FixedLenFeature([], tf.int64),
                                                        'img': tf.FixedLenFeature([], tf.string),})
    img = tf.decode_raw(features["img"], tf.uint8)
    img = tf.reshape(img, [28,28]) # 恢复图像原始大小
    label = tf.cast(features["label"], tf.int32)

    return img, label

def get_data(file_names):
    label = ['1',]
    img_value = tf.read_file(r'D:\data\tf\mnist_train\1\mnist_train_3.png')
    img = tf.image.decode_image(img_value,channels=3)
    return label, img


def get_batch_data(batchSize):
    # dir_path = r'D:\data\tf\mnist_train\1'
    # file_names = os.listdir(dir_path)
    # file_names_all = []
    # for f in file_names:
    #     file_name = dir_path+'\\'+f
    #     file_names_all.append(file_name)
    #     #print(file_name)
    # fname = ''
    # filename = file_names_all[i:i+batchSize]
    # fileNameQue = tf.train.string_input_producer([filename], shuffle=True)
    # label, image = read_data()
    label, image = get_data('')
    input_queue = tf.train.slice_input_producer([image, label], shuffle=False,num_epochs=1)
    image_batch, label_batch = tf.train.batch(input_queue, batch_size=5, num_threads=1, capacity=64,allow_smaller_final_batch=False)
    return image_batch, label_batch
    # min_after_dequeue = 1000
    # capacity = min_after_dequeue+3*batchSize
    # exampleBatch,labelBatch = tf.train.shuffle_batch([image, label],batch_size=batchSize, capacity=capacity, min_after_dequeue=min_after_dequeue)
    # return exampleBatch,labelBatch


x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, shape=[None, 10])
w = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
y_ = tf.nn.softmax(tf.matmul(x,w) + b)

# w = tf.Variable(tf.zeros(784, 10))
# y = tf.nn.softmax(tf.matmul(x,w) + b)
# y_ = tf.placeholder(tf.float32, [None, 10])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
for i in range(5):
  batch_xs, batch_ys = get_batch_data(5)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float32'))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

# import tensorflow as tf
# import tensorflow.examples.tutorials.mnist.input_data as input_data
# mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
# x = tf.placeholder(tf.float32, [None, 784])
# y_actual = tf.placeholder(tf.float32, shape=[None, 10])
# W = tf.Variable(tf.zeros([784,10]))        #初始化权值W
# b = tf.Variable(tf.zeros([10]))            #初始化偏置项b
# y_predict = tf.nn.softmax(tf.matmul(x,W) + b)     #加权变换并进行softmax回归，得到预测概率
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_actual*tf.log(y_predict),reduction_indies=1))   #求交叉熵
# train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)   #用梯度下降法使得残差最小
#
# correct_prediction = tf.equal(tf.argmax(y_predict,1), tf.argmax(y_actual,1))   #在测试阶段，测试准确度计算
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))                #多个批次的准确度均值
#
# init = tf.initialize_all_variables()
# with tf.Session() as sess:
#   sess.run(init)
#   for i in range(1000):               #训练阶段，迭代1000次
#     batch_xs, batch_ys = mnist.train.next_batch(100)           #按批次训练，每批100行数据
#     sess.run(train_step, feed_dict={x: batch_xs, y_actual: batch_ys})   #执行训练
#     if(i%100==0):                  #每训练100次，测试一次
#       print("accuracy:",sess.run(accuracy, feed_dict={x: mnist.test.images, y_actual: mnist.test.labels}))
