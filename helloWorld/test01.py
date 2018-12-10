#encoding=utf8
import traceback

import pymysql
dbclient = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='investment',
    charset='utf8mb4'
)

def update(record):
    curosr = dbclient.cursor()
    # if ['keyword','mltag','humantag'] not in record.keys():
    #     return
    values = []
    try:
        sql = "UPDATE investdetail SET mltag=%s,humantag=%s,keyword=%s "

        for i in range(20):
            values.append(('mltag'+str(i),'humantag'+str(i),'keyword'+str(i)))# 为什么这样循环最后的结果都是保留最后一个数字19而不是0-19跟Python2.7明显不一样
        print(values)
        exit(0)
        curosr.executemany(sql,values)
        dbclient.commit()
    except:
        print(traceback.print_exc())
        curosr.close()


update({})

import csvkit
import logging
loger = logging.getLogger('csvtoes')
loger.setLevel(logging.DEBUG)
fhandler = logging.FileHandler('d:\data\csvtoes.log')
shandler = logging.StreamHandler()
loger.addHandler(shandler)
loger.addHandler(fhandler)
loger.warn('hello i am debug info 2')
loger.warn('fatal error happened ')
