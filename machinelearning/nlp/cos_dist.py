#encoding=utf8
import numpy as np
import math

#如何计算两个矩阵的相似度？一维矩阵计算，多维矩阵计算？
vector_a = [1,5,8,9,3]
vector_b = [1,9,4,5,7]
vector_c = [1,5,8,9,3,3,5,6,2]
def cal_sim(vector_a,vector_b)->float:
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)#线性代数包求矩阵范数
    # print(denom)
    cos = num / denom
    # print(cos)
    sim = 0.5 + 0.5 * cos
    print(sim)
    return sim
# cal_sim(vector_a,vector_b)

def cal_dist(src, target):
    distance = src - target
    if len(src) == 1:
        euclidean_distance = np.linalg.norm(distance) #求范数，用来计算距离
    else:
        euclidean_distance = np.linalg.norm(distance, axis=1, keepdims=True)
    print(euclidean_distance)
    min_distance = euclidean_distance.min()
    index = np.argmin(euclidean_distance)
    return min_distance, index

#通过计算两个列表间相似的元素数量来计算相似度
def cal_sim_v2(user01,user02):
    count = 0
    for x in user01:
        if x in user02:
            count += 1

    return count / math.sqrt(len(user01) * len(user02))



print(cal_sim_v2(vector_a,vector_c))

def cal_sim__dim2(vect_a,vect_b):
    # vector_a = [[1,5],[2,6]]
    # vector_b = [[1,9],[2,7]]
    # vector_a = np.mat(vector_a)
    # vector_b = np.mat(vector_b)
    # # num = float(vector_a * vector_b.T)
    # denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    pass
#----------------------
# vector_a = [[1,5],[2,6]]
# vector_b = [[1,9],[2,7]]
# vector_a = np.mat(vector_a)
# vector_b = np.mat(vector_b)
# # num = float(vector_a * vector_b.T)
# denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)