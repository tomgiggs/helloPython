import re
import redis
import bs4
file=open("E:/hesult2/28100018.txt")
patten='https://www.zhihu.com/people/\S+["$]'
#print file.read()
result=re.findall(patten,file.read())
url="url"
i=0
for x in result:
     i=i+1
     r = redis.Redis(host='localhost', port=6379, db=0)
     r.set("url"+str(i),x.encode())
     r.sadd("url")
     #img= re.match("https://\S+$",x)
     # print img.group()
     print

