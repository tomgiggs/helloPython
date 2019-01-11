#encoding=utf8
import time
import redis
from ssdb import SSDB

rclient = redis.Redis(host="*", port=36379, password='**')
rpipeline = rclient.pipeline()

pipe_time = time.time()
for x in range(10000):
    rpipeline.lpop('task_list_test01')
#rpipeline.lrange('task_list_test01',0,10000)
records = rpipeline.execute()
print('redis total time:',time.time()-pipe_time )

sclient = SSDB('*',port=46379)
# sclient = SSDB(host='18.196.*.*',port=46379,)
sclient.execute_command('auth xxxxxxx')
i = 1
begin_time = time.time()
sclient.qpush_front('task_list_sorted',records)
print(time.time() - begin_time)

exit(0)
for record in records:
    # sclient.zset('task_list_sorted',record,i)
    sclient.qpush_front('task_list_sorted',record)
    i += 1
print(time.time() - begin_time)
#------------------------------------
#postgresql连接代码
import psycopg2

client = psycopg2.connect(database="investment", user="postgres", password="cyl123", host="127.0.0.1", port="5432")
cursor = client.cursor()
cursor.execute("SELECT PROJ_ID,INDUSTRY_ID,PROJ_NAME,PROJ_APP,TOTAL_INVESTMENT,APPLICATE_AREA,BUILD_AREA,BUILD_ADDRESS,LINKMAN  FROM test004 limit 10")
result = cursor.fetchall()
for r in result:
    print(r)
#--------------------------------------
#sqlite3连接代码
import sqlite3
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('user.db')
conn.row_factory = dict_factory
#conn.execute("CREATE TABLE user_info(ID INT PRIMARY KEY  NOT NULL, NAME TEXT  NOT NULL, PASSWD  INT   NOT NULL, ADDRESS CHAR(50) );")
cursor = conn.cursor()
#cursor.execute("insert into user_info values (2,'test02','123456','fujian,zhanghzou')",)
#conn.commit()
table = cursor.execute('select * from user_info')
ta = table.fetchall()

for x in ta:
    print(x)

#encoding=utf8
# import sqlite3
# connection = sqlite3.connect('./instance/user.db')
# cursor = connection.cursor()
# cursor.execute('select * from user')
# results = cursor.fetchall()
# for r in results:
#     print(r)
# print(results)
#----------------
#mysql 连接代码
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
#-----------------


