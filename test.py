#-*- coding: UTF-8 -*-
import  redis
import urllib
import logging
import re
import chardet
from bs4 import BeautifulSoup
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
zhihu = redis.Redis(host="127.0.0.1", port=6379, db=0)
usr=zhihu.smembers('urls')
print usr

file=open('E:/usr.txt','w+')
for x in usr:
    file.write(x)

    file.write('\n')
file.close()

header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
'Connection':'Keep-Alive',
}
'''
#page=urllib.urlopen('https://www.zhihu.com/people/xiao-ai-gua-15-55/activities',None,header).read()
#print page
''''''
def cleanComment():
    # logging.error('this is a info')
    output = open('e:\out.txt', 'a')
    client = pymongo.MongoClient('localhost', 27017, )
    getContent = client.crawl
    allcomment = getContent.comments.find()
    for x in allcomment:
        text = x['commemt']
        content = re.sub('<[\s\S]+?>', '', text, re.U, re.M)
        content = re.sub('</[\s\S]+?>', '', content, re.U, re.M)
        print content
        output.write(content)
def cleanComments2():

    source = open(r'e:\out.txt', 'r+').read()
    print source
    ss = chardet.detect(source)
    print ss
    #source = source.decode('GB2312').encode('utf-8')
    content = re.sub('<\S|\s+?>', '', source)
    content = re.sub('</\S|\s|\w+?/+?>', '', content)


    print content
    # source=source.decode('utf-16').encode('utf-8')
    # dealed=BeautifulSoup(source,'lxml')
    # content=dealed.div(class_='review-content clearfix')

#cleanComments2()

def getStopWord():
    file=open('d:\stopwords.txt','r')
    stoplist=[]
    print file.readline()
    for y in file.readlines():
        #print y
        stoplist.append(y)

    '''
    while(file.readline()):
        x=file.readline()
        stoplist.append(x)
      '''
    for x in stoplist:
        print x.decode('GB2312').encode('utf-8')

#getStopWord()


#content=re.sub('<.+?>','',source,re.DOTALL,re.S)
#content=re.sub('</.+?>','',content,re.DOTALL,re.S)





'''


tags=re.sub(r'<[\s\S]+>','',source,re.U)
result=open('e:resul.txt','w')
result.write(tags)
result.close()
print tags
'''



