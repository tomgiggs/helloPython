# encoding=utf8
'''
tensorboard是使用TensorFlow运行过程中保存的数据来显示运行过程的，如果在运行过程中不保存数据是没有数据可以查看的。
代码开始运行可以使用 tensorboard --logdir logs 启动tensorboard面板，然后使用http://localhost:6006或者复制tensorboard给出的地址在浏览器查看页面
如果启动不了报错OSerror 就修改XXX\site-packages\tensorboard\manager.py
serialize=lambda dt: int((dt - datetime.datetime.fromtimestamp(0)).total_seconds()),=====> serialize=lambda dt: int(dt.strftime('%S')),就可以启动了
滚动滚轮放大图，双击图中节点可以看到每个图更具体的内容。
在面板上点击histograms可以查看变量变化情况，在面板scalars可以看到函数收敛情况（损失函数下降情况）
使用tensorflowjs_converter  将模型转换成可供js读取的模型，教程在这https://www.tensorflow.org/js/tutorials/conversion/import_saved_model
安装官网给出的样例命令死活执行不成功，最后只能自己去源码看命令行的解析是什么样的，Linux下先找到包放置的位置：
先找到命令行的内容：
whereis tensorflowjs_converter
vi /usr/local/bin/tensorflowjs_converter
看到引用了 from tensorflowjs.converters.converter import main
找到包位置，进入文件：
vi /usr/local/lib/python3.6/dist-packages/tensorflowjs/converters/converter.py
最后看到需要的参数形式：
tensorflowjs_converter --input_format=tf_saved_model --output_format='tfjs_graph_model' --saved_model_tags=serve  ./ckpt ./web_model
还是报错OSError: SavedModel file does not exist at: ./ckpt/{saved_model.pbtxt|saved_model.pb}
问题是我保存的模型没有.pb文件。。。。
-------
python3 saved_model_cli.py show --dir=model2/  --all 用来查看.pb文件里面模型的信息：模型的输入/输出的名称、数据类型、shape以及方法名称
python3 saved_model_cli.py show --dir=models/ --tag_set serve --signature_def serving_default

'''

import tensorflow as tf
import numpy as np
# tf.logging.set_verbosity(tf.logging.INFO)

with tf.name_scope(
        'data'):  # 给变量起名，不然在页面无法知道数据对应关系，name_scope不会作为tf.get_variable变量的前缀，但是会作为tf.Variable的前缀，在variable_scope的作用域下，
    # tf.get_variable()和tf.Variable()都加了scope_name前缀。因此，在tf.variable_scope的作用域下，通过get_variable()可以使用已经创建的变量，实现了变量的共享。
    # TF中有两种作用域类型
    # 命名域 (name scope)，通过tf.name_scope 或 tf.op_scope创建；
    # 变量域 (variable scope)，通过tf.variable_scope 或 tf.variable_op_scope创建；
    # 这两种作用域，对于使用tf.Variable()方式创建的变量，具有相同的效果，都会在变量名称前面，加上域名称。
    # 对于通过tf.get_variable()方式创建的变量，只有variable scope名称会加到变量名称前面，而name scope不会作为前缀，variable_scope 可以添加reuse=True属性
    x_data = np.random.rand(666).astype(np.float32)
    y_data = 0.3 * x_data + 0.6

with tf.name_scope('param') as scope:
    weight = tf.Variable(
        tf.random_uniform([1], -1.0, 1.0))  # tf.Variable会重复创建变量，tf.get_variable( )会先查找变量，不存在再创建，存在就直接使用
    bias = tf.Variable(tf.zeros([1]))
    print(bias.name)
    tf.summary.histogram('bias', bias)
    tf.summary.histogram('weight', weight)  # 添加这个语句才能输出变量变化情况
with tf.name_scope('y_target') as scope:
    y_prediction = weight * x_data + bias
with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.square(y_data - y_prediction))
optimizer = tf.train.GradientDescentOptimizer(0.5)
with tf.name_scope('train') as scope:
    train = optimizer.minimize(loss)
    tf.summary.scalar('loss', loss)  # 这个输出函数收敛（节点）情况
with tf.name_scope('init') as scope:
    init = tf.global_variables_initializer()
sess = tf.Session()
writer = tf.summary.FileWriter("./logs/", sess.graph)  # 添加这个语句才能保存运行的图，这个会在图创建完成就保存，不需要等到开始运行再保存

sess.run(init)
merged = tf.summary.merge_all()  # 将所有summary全部保存到磁盘，以便tensorboard显示。如果没有特殊要求，一般用这一句就可一显示训练时的各种信息了。

for var in tf.global_variables():
    print(var.name)
print('-----------------')

for v in tf.trainable_variables():
    print(v.name)

options = tf.RunOptions(output_partition_graphs=True)  # 打印运行时参数
metadata = tf.RunMetadata()
# tf.logging.info("begin training.....")
for step in range(201):
    sess.run(train, options=options, run_metadata=metadata)
    rs = sess.run(merged)
    writer.add_summary(rs, step)  # 将数据写出，不然是获取不到数据的

    if step % 20 == 0:
        print(step, 'weight:', sess.run(weight), 'bias:', sess.run(bias))
# print(metadata.partition_graphs)
sess.close()
