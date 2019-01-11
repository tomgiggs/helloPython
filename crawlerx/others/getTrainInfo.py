#encoding=utf8
from urllib import request
import bs4
import pymongo


url = "http://search.huochepiao.com/chaxun/resultc.asp?txtCheci=k03&cc.x=0&cc.y=0"

def parse(page):
    input = open(r'd:\data\train.html', 'r')
    hpage = bs4.BeautifulSoup(page,'lxml')
    hpage.find_all('')


    pass


def getPage(url,code):

    client = request.urlopen(url)
    html = str(client.read(), encoding = "gbk")
    print(html)
    mongo = pymongo.MongoClient('127.0.0.1',port=27017)
    db = mongo.train
    record = db.record_page
    record.insert({code:html})
getPage(url,'k03')


def getAll():
    train_type = ['K','Z','D','G']
    for t in train_type:
        for i in range(1000):
            code = t + str(i)
            url = "http://search.huochepiao.com/chaxun/resultc.asp?txtCheci="+code+"&cc.x=0&cc.y=0"
            getPage(url,code)


    #print(html)
    # output = open(r'd:\data\train.html','a')
    # output.write(html)

#getAll()
import cookielib
import urllib2
filename="D:\cookie.txt"
cookie=cookielib.MozillaCookieJar(filename)

handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)
respone=opener.open("https://www.zhihu.com/")
cookie.save()

