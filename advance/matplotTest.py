#encoding=utf8
import matplotlib
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import pandas
import numpy as np

# x = numpy.random.random(20)
# x.sort()
# y = numpy.random.random(20)
# y.sort()
# pl.plot(x,y)
# pl.show()

#饼图
def draw_pie():
    # labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # data = np.random.rand(7) * 100
    raw = open('datas.txt', 'r')
    data = []
    labels = []
    stop = 0
    for line in raw.readlines():
        reviews, count = line.split()
        data.append(count)
        labels.append(reviews)
        if stop > 20:
            break
        stop += 1
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.legend()
    plt.show()

#draw_pie()
#bar image
def draw_bar():

    # data = np.random.randint(low=0, high=100, size=N)

    # labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    raw = open('datas.txt','r')
    data = []
    lebels = []
    stop = 0
    for line in raw.readlines():
        reviews, count = line.split()
        data.append(int(count))
        lebels.append(int(reviews))
        # if stop > 50:
        #     break
        # stop += 1

    print(data)
    print(lebels)
    N = len(data)
    x = np.arange(N)
    colors = np.random.rand(N * 3).reshape(N, -1)
    plt.title("reviews range Data")
    #plt.bar(x, data[1:], alpha=0.8, color=colors, tick_label=lebels[1:])
    # plt.scatter(lebels,data)
    plt.show()

draw_bar()

def draw_line():
    raw = open('datas.txt','r')
    data = []
    x = np.arange(3262)
    lebels = []
    stop = 0
    for line in raw.readlines():
        reviews, count = line.split()
        data.append(int(count))
        lebels.append(int(reviews))
        # if stop > 100:
        #     break
        # stop += 1

    print(data)
    print(lebels)
    plt.title("Weekday Data")
    plt.plot(x,lebels)
    plt.plot(x,data,'r')
    plt.show()
#draw_line()