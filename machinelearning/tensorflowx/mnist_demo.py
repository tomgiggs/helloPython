import tensorflow as tf
from tensorflow.examples.tutorials.mnist import mnist
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.framework import graph_util
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

#摘自官网
def mnist_demo():
    mnist = input_data.read_data_sets(r'E:\dataset\tf_data') # 读取数据，如果没有就下载
    x = tf.placeholder(tf.float32, [None, 784],'x') # 使用占位符声明后面变量会存储的数据类型及维度信息等（因为底层用C实现，
    # x = tf.get_variable('x',[None, 784],tf.float32)

    # 所以需要类型信息，还有维度信息（创建多维数组要用到））
    # W = tf.Variable(tf.zeros([784, 10]))
    # W = tf.get_variable('w',tf.zeros([784, 10]),) #这样写不行
    W = tf.get_variable('w', [784, 10],tf.float32,tf.zeros_initializer,)
    b = tf.Variable(tf.zeros([10]))
    # b = tf.get_variable('b',tf.zeros([10])) #这样写不行
    # b = tf.get_variable('b', [10],tf.zeros_initializer)
    y = tf.matmul(x, W) + b #定义算法（目标函数）
    y_ = tf.placeholder(tf.int64, [None],'y_') #声明标记数据的维度
    # y_ = tf.get_variable('y_',[None],tf.int64)
    cross_entropy = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=y) #定义计算损失函数
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)# 计算损失函数的具体方式
    sess = tf.InteractiveSession()#创建会话
    tf.global_variables_initializer().run() #启动图，开始计算
    saver = tf.train.Saver(max_to_keep=5) #模型保存器
    #模型操作 官方说明https://www.tensorflow.org/guide/saved_model#overview_of_saving_and_restoring_models
    for s in range(30):
        batch_xs, batch_ys = mnist.train.next_batch(100) #获取训练数据
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys}) #开始训练
        saver.save(sess, 'ckpt2/mnist.tfmodel', global_step=s+1) #保存模型，但是好像并不能用。。其中字符串为保存模型的前缀,这个方法生成的数据分为四个文件，下面的代码时直接生成一个文件
        #模型保存方法2
        # if s==29:
        #     graph_def = tf.get_default_graph().as_graph_def()
        #     output_graph_def = graph_util.convert_variables_to_constants(sess,graph_def, ['add'])
        #     with tf.gfile.GFile("ckpt/combined_model.pb", 'wb') as f:
        #         f.write(output_graph_def.SerializeToString())
        #模型保存方法3
        # if s==29:
        #     builder = tf.saved_model.builder.SavedModelBuilder('./models')
        #     builder.add_meta_graph_and_variables(sess, [tf.saved_model.tag_constants.SERVING])
        #     builder.save()
        ##执行tensorflowjs_converter --input_format=tf_saved_model --output_format='tfjs_graph_model' --saved_model_tags=serve  ./model2 ./web_model  报错KeyError: 'serving_default'

        #保存方法4
        if s == 29:
            builder = tf.saved_model.builder.SavedModelBuilder('model6')
            signature = predict_signature_def(inputs={'input': x}, outputs={'output': y})
            builder.add_meta_graph_and_variables(sess, [tf.saved_model.tag_constants.SERVING],signature_def_map={'predict': signature})
            builder.save()
        #  tensorflowjs_converter --input_format=tf_saved_model --output_format='tfjs_graph_model' --saved_model_tags=serve --signature_name=predict  ./model2 ./web_model
        #报错：tensorflow.python.framework.errors_impl.InvalidArgumentError: Failed to import metagraph, check error log for more info

        # checkpoint文件保存了一个目录下所有的模型文件列表，这个文件是tf.train.Saver类自动生成且自动维护的。
        # .meta文件保存了TensorFlow计算图的结构，可以理解为神经网络的网络结构 ，TensorFlow通过元图（MetaGraph）来记录计算图中节点的信息以及运行计算图中节点所需要的元数据。
        # .data - 00000 - of - 00001 文件保存了TensorFlow程序中每一个变量的取值，这个文件是通过SSTable格式存储的，可以大致理解为就是一个（key，value）列表。
        # .index是对应模型的索引文件
        # MetaGraphDef  是一个协议缓冲区，用于定义图所支持的计算的签名。常用的输入键、输出键和方法名称
        # SignatureDef ,
        # Estimator 训练 Estimator 模型之后，您可能需要使用该模型创建服务来接收请求并返回结果。您可以在本机运行此类服务，或在云端部署该服务,要准备一个训练过的 Estimator 以供使用，您必须以标准 SavedModel 格式导出它



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