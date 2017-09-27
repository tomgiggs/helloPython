#-*- coding: UTF-8 -*-
import requests
import urllib
import re
from bs4 import BeautifulSoup
url='http://31f.cn/'
header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
'Connection':'Keep-Alive',
}

''''''
#result=urllib.urlopen(url,None,header).read()
file=open("E:/proxy.txt",'a+')
#file.write(result)
result=file.read()
res = re.sub('<td><a href=.*</td>', ' ', result)
#files=open("E:/proxies.txt",'a+')
#files.write(res)
ips=re.findall('(\d+\.){4}',result)
print ips
'''
soup=BeautifulSoup(res,'lxml')
ok=soup.find_all(
'table')
'''
#xxx=re.findall('<td><a href=.*</td>',ok)
'''
#files=open("E:/proxies.txt",'a+')

for y in ok:
    print y
'''
'''
#print result
soup=BeautifulSoup(result,'lxml')
ok=soup.find_all('table')

#xxx=re.findall('<td><a href=.*</td>',ok)
files=open("E:/proxies.txt",'a+')
for y in ok:
    print y
    files.writelines(y)
#res=re.findall('<td>*.+</td>',result)
#res=re.findall('<td><a href=*</td>',ok)
#print res
#rex=re.findall('<td><a href=.*</td>',result)
#print ok

'''
'''
for x in ok:
    if not len(re.findall('<td><a href=.*</td>',x)):
        res = re.sub('<td><a href=.*</td>', ' ', x)
        print res
 '''

#for y in res:
    #print y

'''
for x in ok:
    res=re.findall('<td><a href=*</td>',x)
    print x
'''
