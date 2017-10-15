#-*- coding: UTF-8 -*-
import urllib
import urllib2
import chardet
import pymongo

pre_url='http://tianqi.2345.com/t/wea_history/js/'
def getJson():
    for year in range(2016,2017):
        for month in range(1,12):
            date=str(year)+str(month)
                   
            url=pre_url+'/'+date+'/'+'60301_'+date+'.js'
            request =urllib.urlopen(url).read()
            s=request.decode('GB2312').encode('utf-8')
            saveToMongodb(date,s)
            

def saveToMongodb(date,data):
    client=pymongo.MongoClient('localhost',27017)
    db=client.weather
    db.data.insert(
        {
            'date':date,
            'data':data

        }
    )
'''
request =urllib.urlopen('http://tianqi.2345.com/t/wea_history/js/201606/60301_201606.js').read()
#print chardet.detect(request)

s=request.decode('GB2312').encode('utf-8')
print s
'''
getJson()