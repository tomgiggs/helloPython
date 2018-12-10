import  urllib
from bs4 import BeautifulSoup
import pymongo
import  time

client=pymongo.MongoClient('localhost',27017)
crawl=client.crawl
def getComments():
    pass


preurl='https://movie.douban.com/subject/25808075/reviews'
comments=set()
for y in range(1,50):
    url=preurl+'?start='+str(y*20)
    time.sleep(0.25)
    page=urllib.urlopen(url).read()
    data = BeautifulSoup(page, 'lxml')
    dots = data.findAll('div', class_='short-content')
    for x in dots:
        if x.a:
            hrefs = x.a.get('href')
        if hrefs != 'javascript:;':
            # print hrefs
            comments.add(hrefs)


#print comments
def getDetailComment():
    sleep=1
    while len(comments):
        sleep+=1
        time.sleep(0.25)
        try:
            link = comments.pop()
            #print link
            pages = urllib.urlopen(link).read()
            #print pages
            detail = BeautifulSoup(pages, 'lxml')
            result = detail.find('div', class_='main-bd')
            print(result)

            crawl.comments.insert({
                'source':pages,
                'comment_url': link,
                'commemt': str(result)
            })
        except:
            pass



getDetailComment()
client.close()



