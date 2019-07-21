# import tensorflow as tf
#
# print(tf.zeros([1]))
# import pip
# print(pip.pep425tags.get_supported())
import os
dir_path = r'D:\data\tf\mnist_train\1'
file_names = os.listdir(dir_path)
for f in file_names:
    file_name = dir_path+'\\'+f
    print(file_name)


