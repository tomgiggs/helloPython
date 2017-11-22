#-*- coding: UTF-8 -*-
import re
import redis
import urllib
import urllib2
#from bs4 import BeautifulSoup
import MySQLdb
import time
import pymongo
import threading
import thread
import random
import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
'Connection':'Keep-Alive',
}
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zhihuUser.log',
                filemode='w')
filepath="e:\zhihu/"
people_url='https://www.zhihu.com/people/\S+["$]'
source="https://www.zhihu.com/question/"

client=pymongo.MongoClient("localhost",27017)
db=client.zhihu
zhihu = redis.Redis(host="127.0.0.1", port=6379, db=0)
#datas=db.user.find()

#proxies=['80.107.117.210:3128','93.91.112.185:80','158.140.175.104:8080','80.252.148.148:8080','195.34.241.85:8080']
#x=random.randint(0,9)

conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='zhihu_info', port=3306)
'''for x in datas:
    if x.get("url")!=None:
        print x.get("url")
'''

def getUser():
    times = 1
    for x in range(48000000,48001010):
        #xxx = random.randint(0, 4)
        times+=1
        if times%10==0:
            time.sleep(1)
        '''
        proxy_handler = urllib2.ProxyHandler({'http': proxies[xxx]})
        opener = urllib2.build_opener(proxy_handler)
        page = opener.open(source+str(x))
        '''
        #print(r.read())

        page=urllib.urlopen(source+str(x),None,header).read()
        #print page
        '''
        db.pages.insert({
            'question_id':x,
            'content':page
            })
        '''

        #file=open(filepath+str(x)+".html","r+").read()
        urls=re.findall(people_url,page)
        for y in urls:

            #re.split(r'" ',y)
            y=y[:-1]
            zhihu.sadd("urls",y)
            #print y
def getUserInfo():
    #save usr_links to file
    usr = zhihu.smembers('urls')
    file = open('E:/usr.txt', 'w+')
    for x in usr:
        file.write(x)
        file.write('\n')
    file.close()

    sleep=1
    for x in zhihu.smembers("urls"):
        #yyy = random.randint(0, 4)
        sleep+=1
        if sleep%10==0:
            time.sleep(1)
            url = zhihu.spop('urls')
            info = urllib.urlopen(url, None, header).read()
            '''
            
            proxy_handler = urllib2.ProxyHandler({'http': proxies[yyy]})
            opener = urllib2.build_opener(proxy_handler)
            info = opener.open(source + str(x))
            '''
            '''
            soup=BeautifulSoup(info,'lxml')
            care = soup.find_all('div', class_='NumberBoard-value')
            good = soup.find_all('div', class_='Profile-sideColumnItemValue')
            '''
            try:
                name = re.split(r'/', url)[4]
                care_num = re.findall(r'<div class="NumberBoard-value">\d+', info)
                if care_num:
                    care = re.sub(r'\D', '', care_num[1])
                else:
                    care = 0
                    agree_num = re.findall(r'获得 \d+ 次赞同', info)
                if agree_num:
                   agree = re.split(' ', agree_num[0])[1]
                else:
                    agree = 0
                thank_num = re.findall(r'获得 \d+ 次感谢', info)
                if thank_num:
                    thank = re.split(' ', thank_num[0])[1]
                else:
                    thank = 0
                    collection_num = re.findall(r'\d+ 次收藏', info)
                if collection_num:
                    be_collectioned = re.split(' ', collection_num[0])[0]
                else:
                    be_collectioned = 0
                # print agree,care,be_collectioned
                infoList = [name, care, agree, thank, be_collectioned]
                insertToMysql(infoList)
            except ValueError:
                pass
            '''
            db.userpage.insert({
                'question_id': name,
                'content': info
            })
            db.user.insert({
                'user_name': name,
                'care_number': care,
                'thank_number': thank,
                'agree_nuber': agree,
                'collectioned': be_collectioned
            })'''

def insertToMysql(list):

    cur = conn.cursor()
    sql="insert into user(name,care_num,agree_num,thank_num,collection_num)values('%s',%s,%s,%s,%s)"%(list[0],list[1],list[2],list[3],list[4])
    cur.execute(sql)
    conn.commit()
    cur.close()

def sendMail():
    sender='zamjbn@163.com'
    receiver = '1369796093@qq.com'
    message = MIMEText('爬虫已经爬去完成，可以下载数据了.', 'plain', 'utf-8')
    message['From'] = Header(sender)
    message['To'] = Header(receiver)
    subject = 'Python 邮件通知'
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP_SSL("smtp.163.com")
    smtpObj.login(sender, 'cyl0516')
    smtpObj.sendmail(sender, receiver, message.as_string())
    smtpObj.quit()
    print "邮件发送成功"

def createTable():
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='zhihu_info', port=3306)
        cur = conn.cursor()
        sql = 'create table user_INFO(id INT NOT NULL AUTO_INCREMENT,   name VARCHAR(50) NOT NULL,care_num VARCHAR(10) ,  agree_num VARCHAR(10),thank_num VARCHAR(10) NOT NULL, collection_num VARCHAR(10) NOT NULL,  PRIMARY KEY ( id ));'
        cur.execute(sql)
        cur.close()
        conn.close()
        print 'success'

    except:
        cur.close()
        conn.close()
        print 'fail'
createTable()
getUser()
getUserInfo()
sendMail()


