#encoding=utf8
'''
tensorflow 数据集工具
'''
import tensorflow_datasets as tfds
import tensorflow as tf

def get_ds_info():
    print(tfds.list_builders())
    for ds_name in tfds.list_builders():
        ds = tfds.builder(ds_name)
        print(ds.info)



# tf.enable_eager_execution()
def get_ds_batch(ds_name):
    ds_train, ds_test = tfds.load(name="mnist", split=["train", "test"])
    ds_train = ds_train.shuffle(1000).batch(128).prefetch(10)
    for features in ds_train.take(1):
      image, label = features["image"], features["label"]
      yield image,label
     #或者这样使用
    # mnist_builder = tfds.builder("mnist")
    # mnist_builder.download_and_prepare()
    # ds = mnist_builder.as_dataset(split=tfds.Split.TRAIN)

