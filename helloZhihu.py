#-*- coding: UTF-8 -*-
import re
import redis
import urllib
import urllib2
from bs4 import BeautifulSoup

header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
'Connection':'Keep-Alive',
}
filepath="e:\zhihu/"
people_url='https://www.zhihu.com/people/\S+["$]'
source="https://www.zhihu.com/question/"
import pymongo
client=pymongo.MongoClient("localhost",27017)
db=client.zhihu
zhihu = redis.Redis(host="127.0.0.1", port=6379, db=0)
#datas=db.user.find()
'''for x in datas:
    if x.get("url")!=None:
        print x.get("url")
'''
def getUser():
    for x in range(48000005,48000010):
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
        print y
def getUserInfo():
    url=zhihu.spop('urls')
    info=urllib.urlopen(url,None,header).read()

    '''
    soup=BeautifulSoup(info,'lxml')
    care = soup.find_all('div', class_='NumberBoard-value')
    good = soup.find_all('div', class_='Profile-sideColumnItemValue')
    '''
    name=re.split(r'/',url)[4]
    care_num = re.findall(r'<div class="NumberBoard-value">\d+', info)
    agree_num = re.findall(r'获得 \d+ 次赞同', info)
    thank_num = re.findall(r'获得 \d+ 次感谢', info)
    collection_num = re.findall(r'\d+ 次收藏', info)
    thank=re.split(' ', thank_num[0])[1]
    be_collectioned=re.split(' ', collection_num[0])[0]
    agree=re.split(' ', agree_num[0])[1]
    care=re.sub(r'\D', '', care_num[1])
    print agree,care,be_collectioned
    db.userpage.insert({
        'question_id': name,
        'content': info
    })
    db.user.insert({
        'user_name':name,
        'care_number':care,
        'thank_number':thank,
        'agree_nuber':agree,
        'collectioned':be_collectioned
    })
getUser()
getUserInfo()


