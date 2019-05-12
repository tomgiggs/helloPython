# encoding=utf8
import numpy as np
from PIL import Image
from pylab import *
from scipy import misc
# 下面操作参考了https://zhuanlan.zhihu.com/p/62703610的操作，主要是讲图片变成一个类似素描的效果


import cv2


def cvt_photo(img):
    # cv2.imshow('origin', img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 将图片变为黑白灰度图

    img_blurred = cv2.GaussianBlur(img_gray, (3, 3), 0)  # 将图片做高斯模糊，第二个参数是一个奇数数组，叫高斯核的尺寸，这个核尺寸越大图像越模糊

    cv2.imshow('bulerd', img_blurred)  # 第一个参数是窗口标题
    # 整体上做这个就是一个调参的过程，找到一系列合适的参数将图片变成自己想要的效果
    img_threshold1 = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3,
                                           1)  # 对图片进行二值化转化，，像素值大于等于某个值的都直接设为最大值，小于这个值的都直接设为最小值
    cv2.imshow('thresholded', img_threshold1)
    img_threshold1_blurred = cv2.GaussianBlur(img_threshold1, (5, 5), 0)  # 再进行一次模糊处理

    _, img_threshold2 = cv2.threshold(img_threshold1_blurred, 200, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 获取一个图像开运算的核
    img_opening = cv2.bitwise_not(
        cv2.morphologyEx(cv2.bitwise_not(img_threshold2), cv2.MORPH_OPEN, kernel))  # 将图片的颜色进行黑白颠倒使得开运算效果更好
    img_opening_blurred = cv2.GaussianBlur(img_opening, (3, 3), 0)  # 再做一次模糊处理
    cv2.imshow('img_opening', img_opening)  # 最后展示一下，做的过程中可以使用断点来调参数
    return img_opening_blurred


def process_video(path=None):
    '''
    这个函数是用来处理视频的
    :param path: 视频地址
    :return:
    '''
    video = cv2.VideoCapture(
        './videoplayback.mp4')  # 报错warning: Error opening file (../../modules/highgui/src/cap_ffmpeg_impl.hpp 的话就有移动一下文件路径
    np.set_printoptions(threshold=np.inf)
    while video.isOpened():
        ret, frame = video.read()
        if ret is True:
            cvted = cvt_photo(frame)
            cv2.imshow('cvt_video', cvted)
            if cv2.waitKey(25) & 0xFF == ord('q'):  # waitKey函数用于控制显示帧率，后面的条件是判断是否有按下q推出视频
                break
        else:
            break

    video.release()  # 关闭视频
    cv2.destroyAllWindows()


def resize_video():
    video = cv2.VideoCapture(
        './videoplayback.mp4')  # 报错warning: Error opening file (../../modules/highgui/src/cap_ffmpeg_impl.hpp 的话就有移动一下文件路径
    np.set_printoptions(threshold=np.inf)
    while video.isOpened():
        ret, frame = video.read()
        if ret is True:
            cv2.putText(frame, "好好学习，天天吃土", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 125))  # 添加文字
            arrays = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            print(arrays.shape)  # 看看图片是一个什么样的数据
            arrays = cv2.resize(arrays, (480, 270))  # 改变大小
            # cv2.rotate(arrays,rotateCode=0) #旋转视频
            arrays = np.transpose(arrays)
            print(arrays)
            print(arrays.shape)
            cv2.imshow('Frame', arrays)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


def read_img_by_np():
    # img = np.load(r'./iceage.jpg') #OSError: Failed to interpret file 'D:\\data\\tf\\mnist_train\\1\\mnist_train_3.png' as a pickle
    # image to numpy array
    img = Image.open('./iceage.jpg')
    img_array = Image.fromarray(uint8(img))  # <PIL.Image.Image image mode=L size=28x28 at 0xBD4ECF8>
    img_np = np.array(img_array)  # ok
    # numpy array to image
    # img_out = misc.toimage(img_np)
    # img_out.show()
    img = Image.fromarray(img_np)
    img.save('./array_to_img.jpg')  # save image as a file

# img = cv2.imread('iceage.jpg') #读取图片
# cvt_photo(img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()#关闭所有图像显示
