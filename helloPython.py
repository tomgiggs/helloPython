
import re
from bs4 import BeautifulSoup
import urllib
html=urllib.urlopen("http://www.cnblogs.com/fnng/p/3576154.html").read()
#print html
soup=BeautifulSoup(html,"lxml")
page=open("D:\workspace\helloPython\page2.txt","a+")
div=soup.find_all("div",class_="entry")
for d in div:
    #print d.encode("utf-8")
    #page.write(d.encode("utf-8"))
#page.write(soup.encode("utf-8"));
#print soup.title.string
#piss=soup.find_all("p")
#for p in piss:
 #   print p.encode("utf-8")
 soup2=open("D:\workspace\helloPython\page2.txt","r+")
 print soup2.read()
result=BeautifulSoup(soup2,"lxml")
result.find_all("p")
#for res in result:

#print res.encode("utf-8")