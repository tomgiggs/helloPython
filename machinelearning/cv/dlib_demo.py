# encoding=utf8
import sys, os, dlib, glob
import numpy as np
import json
from skimage import io  # pip install scikit-image

import cv2

predictor_path = "shape_predictor_68_face_landmarks.dat"
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"
faces_folder_path = "./"

detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
descriptors = []


def get_face_feature(img_path):
    descriptors = []
    img = io.imread(img_path)
    faces = detector(img, 1)
    print("Number of faces detected: {}".format(len(faces)))
    # print(faces[0]) #rectangles[[(1019, 502) (1685, 1168)]]
    for k, d in enumerate(faces):
        shape = shape_predictor(img, d)  # <dlib.full_object_detection object at 0x7f3e2512bb58>
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        v = np.array(face_descriptor)  # 不是说68个关键点吗，为什么会有128个值？
        descriptors.append(v)
    # print(descriptors)
    return descriptors


def tag_face(img_path):
    img = io.imread(img_path)
    faces = detector(img, 1)
    print("Number of faces detected: {}".format(len(faces)))
    face = faces[0]
    border = np.zeros(4, dtype=np.int32)
    border[0] = np.maximum(face.left(), 0)  # 取最大值
    border[1] = np.maximum(face.top(), 0)
    border[2] = np.minimum(face.right(), img.shape[1])  # 取最小值
    border[3] = np.minimum(face.bottom(), img.shape[0])
    cv2.rectangle(img, (border[0], border[1]), (border[2], border[3]), (0, 255, 0), 2)  # 圈出人脸范围

    facepoint = np.array([[p.x, p.y] for p in shape_predictor(img, faces[0]).parts()])
    # 标记出特征点
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(68):
        cv2.circle(img, (facepoint[i][0], facepoint[i][1]), 1, (0, 225, 0), 2)
        #     #img[facepoint[i][1]][facepoint[i][0]] = [255, 0, 0]
        cv2.putText(img, str(i + 1), (facepoint[i][0], facepoint[i][1]), font, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
    io.imsave('taged2.jpg', img)
    # cv2.imwrite('taged.jpg')


# 计算最相似的人脸，来源于https://codeload.github.com/buptlj/face
def find_most_likely_face(face_descriptor, faces):
    # labels = [key for key in faces.keys()]
    labels = list(faces.keys())
    values = [np.array(value) for value in faces.values()]
    face_distance = face_descriptor - values  # unsupported operand type(s) for -: 'float' and 'dict_values'
    if len(labels) == 1:
        euclidean_distance = np.linalg.norm(face_distance)  # 求范数，用来计算距离
    else:
        euclidean_distance = np.linalg.norm(face_distance, axis=1, keepdims=True)
    min_distance = euclidean_distance.min()
    print('distance: ', min_distance)
    if min_distance > 0.4:
        return 'other'
    index = np.argmin(euclidean_distance)
    return labels[index]


def cal_dist(src, target):
    distance = src - target
    if len(src) == 1:
        euclidean_distance = np.linalg.norm(distance)  # 求范数，用来计算距离
    else:
        euclidean_distance = np.linalg.norm(distance, axis=1, keepdims=True)
    print(euclidean_distance)
    min_distance = euclidean_distance.min()
    index = np.argmin(euclidean_distance)
    return min_distance, index


def recognize_all():
    data_path = './'
    record = {}
    for f in os.listdir(data_path):
        if f.find("jpg") == -1 or f == " ":
            continue
        print(f)
        record[f] = get_face_feature(f)[0].tolist()

    output = open('record.json', 'a+')
    output.write(json.dumps(record))


'''
到这里就可以顺利识别出人脸了，但是要应用的话应该怎么做才能最快找出相似人脸？可不可以像坐标系一样定一个基准坐标点（简称：标准人脸），其他人脸都向基准坐标看齐，然后计算出每个人脸与标准人脸的距离，
要识别A就先找跟A与标准人脸距离差不多的人脸数据，直接返回与A距离最近的人脸数据？
'''


def recognition(src_img):
    features = open('record.json', 'r').read()
    features = json.loads(features)
    src_face = get_face_feature(src_img)[0]
    who = find_most_likely_face(src_face, features)
    print(who)
    return who


recognition()
# print(get_face_feature('./train.jpg'))
# dlib.hit_enter_to_continue()
# recognize_all()
