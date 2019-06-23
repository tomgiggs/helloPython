#encoding=utf8
import numpy as np

#如何计算两个矩阵的相似度？一维矩阵计算，多维矩阵计算？
vector_a = [1,5,8,9,3]
vector_b = [1,9,4,5,7]
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