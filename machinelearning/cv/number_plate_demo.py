# encoding=utf8
'''
入门图像处理先从OpenCV入手是比较简单的，因为OpenCV提供了很多现成的算法，很多现成的函数进行图像处理，如果一上来就用TensorFlow自己搞肯定是很难受的
这是一个车牌号区域识别的样例代码
本段代码参考了博客：https://blog.csdn.net/eastmount/article/details/81461679
'''
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2

def cvt_photo_simple(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#变成灰度图
    _, bin_demo = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)#二值化让图片变得更简单，第二个参数是控制如何进行二值化（类似于四舍五入，小于第二个参数的变成0，大于的变成255），通过简单控制这个参数就可以获得挺好的效果
    # cv2.imshow("bin_demo", bin_demo)
    return bin_demo


def cvt_photo2(img):
    images = []
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#变成灰度图
    images.append(img_gray)
    gaussian = cv2.GaussianBlur(img_gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)#高斯平滑，
    images.append(gaussian)
    median = cv2.medianBlur(gaussian, 5)
    images.append(median)
    sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3) #边缘检测，边缘和轮廓通常位于图像中灰度突出的地方，因而可以直观的想到用灰度的差分对边缘和轮廓进行提取，通常可以通过梯度算子进行提取。
    # 图像锐化的目的是提高图像的对比度，从而使图像更清晰，通过提高邻域内像素的灰度差来提高图像的对比度。
    images.append(sobel)
    # cv2.imshow('sobel',sobel)
    ret, binary = cv2.threshold(sobel, 150, 255, cv2.THRESH_BINARY) #二值化
    images.append(binary)
    # return binary
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 6))    # 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, element2, iterations=1)    # 腐蚀一次，去掉细节
    images.append(dilation)
    erosion = cv2.erode(dilation, element1, iterations=1)    # 再次膨胀，让轮廓明显一些
    images.append(erosion)
    dilation2 = cv2.dilate(erosion, element2, iterations=3)
    for i in range(len(images)):
        plt.subplot(4, 4, i + 1), plt.imshow(images[i], 'gray')#使用matplotlib来绘制变幻过程中的图像，省得没变换一次就绘制一次图，第一，第二个参数是绘制m*n个图像，第三个参数是绘制在那个位置
        plt.title(i)
        plt.xticks([]), plt.yticks([])
    plt.show()
    return dilation2


def find_number_simple(img):
    # img_cvt = cvt_photo_simple(img)
    img_cvt = cvt_photo2(img)#一堆花里胡哨的操作还不如简单转换效果来得好。。。

    # cv2.imshow("bin_demo", bin_demo)
    contours,hierarchy = cv2.findContours(img_cvt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#提取图片中的小图形（轮廓）
    region = find_region(contours)
    print(len(region))
    for ctr in region:
        cv2.drawContours(img, [ctr], 0, (255, 0, 0), 3)#在原图中绘制计算出来的小图像轮廓，第一个参数image表示目标图像，第二个参数contours表示输入的轮廓组，每一组轮廓由点vector构成，第三个参数contourIdx指明画第几个轮廓，如果该参数为负值，则画全部轮廓，
        # 第四个参数color为轮廓的颜色，第五个参数thickness为轮廓的线宽，如果为负值或CV_FILLED表示填充轮廓内部，第六个参数lineType为线型，第七个参数为轮廓结构信息，第八个参数为maxLevel
        # cv2.imshow("bin_demo", img)
    cv2.imshow("bin_demo", img) #画出来的结果根据二值化的阈值不同而异，当阈值为170时图片中的每个字母都取出来的，但是最大的轮廓歪到姥姥家了，但是阈值换成150马上就获得了很好的效果
    time.sleep(1)


#特征提取规则，后面可以加入更加多样的特征判断规则
def find_region(contours):
    region = []
    for cnt in contours:
        area = cv2.contourArea(cnt)# 计算轮廓的面积
        if area < 1000:#面积太小的就不要了明显不是
            continue
        rect = cv2.minAreaRect(cnt)#在图形中截取面积最小的长方体
        box = cv2.boxPoints(rect)# 计算长方体四个角的坐标
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        ratio =float(width) / float(height) #计算长宽比，比列与车牌相差太大的就不要了
        if ratio > 8 or ratio < 2:
            continue
        ctr = np.array(box).reshape((-1, 1, 2)).astype(np.int32)#或者使用box = np.int0(box)转为int类型，不然后面画图会报错：drawContours '(-215) npoints > 0'
        region.append(ctr)
    return region

img = cv2.imread('./photo/number_plate.jpg') #读取图片
find_number_simple(img)
