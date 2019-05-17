'''
模型的各种操作，保存模型，查看模型里面包含哪些内容，加载模型，对模型进行转换
'''
from tensorflow.python.tools import inspect_checkpoint as chkp
import tensorflow as tf
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

# print all tensors in checkpoint file
# chkp.print_tensors_in_checkpoint_file("ckpt/saved_model.pb", tensor_name='', all_tensors=True)# Unable to open table file ckpt\saved_model.pb: Data loss: not an sstable

#------------------保存模型
# v1 = tf.get_variable("v1", shape=[3], initializer = tf.zeros_initializer)
# v2 = tf.get_variable("v2", shape=[5], initializer = tf.zeros_initializer)
# inc_v1 = v1.assign(v1+1)
# dec_v2 = v2.assign(v2-1)
# init_op = tf.global_variables_initializer()
# saver = tf.train.Saver()
# with tf.Session() as sess:
  #   sess.run(init_op)
  #   inc_v1.op.run()
  #   dec_v2.op.run()
  #   # save_path = saver.save(sess, "tmp/model.ckpt")
  #   # print("Model saved in path: %s" % save_path)
  # builder = tf.saved_model.builder.SavedModelBuilder('model4')
  # builder.add_meta_graph_and_variables(sess, [tf.saved_model.tag_constants.SERVING])
  # builder.save()
#
#-----------------加载模型
# tf.reset_default_graph()
# v1 = tf.get_variable("v1", shape=[3])
# v2 = tf.get_variable("v2", shape=[5])
# saver = tf.train.Saver()
# with tf.Session() as sess:
#   saver.restore(sess, "tmp/model.ckpt")
#   print("Model restored.")
#   print("v1 : %s" % v1.eval())
#   print("v2 : %s" % v2.eval())
#------------
#查看某个检查点中的变量
# chkp.print_tensors_in_checkpoint_file("ckpt2/mnist.tfmodel", tensor_name='', all_tensors=True) # Unsuccessful TensorSliceReader constructor: Failed to find any matching files for ckpt2/mnist.tfmodel，官网是这样的写的但是报错了，只能用来检测.pb文件？？
# chkp.print_tensors_in_checkpoint_file("model6/saved_model.pb", tensor_name='', all_tensors=True) #这个也不行
# chkp.print_tensors_in_checkpoint_file("ckpt2/mnist.tfmodel-26.meta", tensor_name='', all_tensors=True)#这个也不行，报错了
# chkp.print_tensors_in_checkpoint_file("ckpt2/mnist.tfmodel-27.index", tensor_name='', all_tensors=True)# 这个没报错，但是也没有输出
chkp.print_tensors_in_checkpoint_file("./ckpt2", tensor_name='', all_tensors=True) #UnicodeEncodeError: 'utf-8' codec can't encode character '\udcbe' in position 97: surrogates not allowed


#-----------------模型参数恢复测试
# tf.reset_default_graph() #进行模型恢复前先清空图以免数据混乱了
# W = tf.get_variable('w', [784, 10],tf.float32,tf.zeros_initializer,)
# saver = tf.train.Saver() #定义恢复模型的加载器，通过参数来控制恢复哪些变量,没有参数的话全部恢复
# with tf.Session() as sess:
#     # saver = tf.train.Saver({"w": W})#只恢复指定的部分变量
#     W.initializer.run()#只恢复指定的部分变量
#     # saver = tf.train.import_meta_graph('ckpt2/mnist.tfmodel-26.meta') #
#     saver.restore(sess, tf.train.latest_checkpoint("ckpt2/")) #这个只需要前缀，不需要具体的文件或者文件名
#     print('w',W.eval())# 如果里面保存的模型参数没有命名就会找不到然后报错NotFoundError (see above for traceback): Restoring from checkpoint failed.，这个主要是在restore里面指定的参数里面设置，在import_mata_graph里面指定了错误的数据也没事









