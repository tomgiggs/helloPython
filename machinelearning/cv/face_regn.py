# encoding=utf8
'''
这是一段使用OpenCV进行人脸定位的样例代码，先使用这个截取出一批人脸数据，然后再使用人脸数据进行人脸识别训练
'''
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
# import dlib#这个库在Windows上用不了。。。
# import face_recognition#这个库在Windows上用不了，因为它是基于dlib的

def find_face(img):
    model_path = r"D:\toolkit\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(model_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 2, 5)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 0)
        cv2.imshow('find_head', img)
    return

# def find_face_by_dlib(img):
#     image = face_recognition.load_image_file("your_file.jpg")
#     face_locations = face_recognition.face_locations(image)

# img = cv2.imread('./photo/head_photo.jpg') #读取图片
# find_face(img)
def resize(img):
    raw_img = cv2.imread('./photo/avatar/001.jpg')
    ss = cv2.resize(raw_img, (60, 60), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('resize',ss)
    pass

# resize('')

def reshape_demo():
    images = []
    raw_img = cv2.imread('./photo/avatar/0000099/001.jpg')
    # ss = cv2.resize(raw_img, (64, 64), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow('resize',ss)
    images.append(raw_img)
    img_arr=np.array(images)
    print(img_arr.shape)
    img_arr.reshape(-1,32)

# reshape_demo()
def load_cuda():
    import ctypes
    ctypes.WinDLL('cudart64_100.dll')
    pass
load_cuda()
