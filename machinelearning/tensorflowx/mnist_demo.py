import tensorflow as tf
from tensorflow.examples.tutorials.mnist import mnist
from tensorflow.examples.tutorials.mnist import input_data

#摘自官网
def mnist_demo():
    mnist = input_data.read_data_sets(r'E:\dataset\tf_data') # 读取数据，如果没有就下载
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
    saver = tf.train.Saver(max_to_keep=1) #模型保存器
    for s in range(300):
        batch_xs, batch_ys = mnist.train.next_batch(100) #获取训练数据
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys}) #开始训练
        saver.save(sess, 'ckpt/mnist.tfmodel', global_step=s+1) #保存模型
    #恢复模型
    # model_file = tf.train.latest_checkpoint('ckpt/')
    # saver.restore(sess, model_file)

    correct_prediction = tf.equal(tf.argmax(y, 1), y_) # 计算模型预测值与实际值的差距
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) #将每次预测结果转化为数值，然后求平均值
    print(sess.run(
        accuracy, feed_dict={
            x: mnist.test.images,
            y_: mnist.test.labels
        })) # 计算预测准确度



if __name__ == '__main__':
    mnist_demo()