#-*- coding: UTF-8 -*-

import urllib2
import urllib
import time
import selenium
from selenium import webdriver
import re
from bs4 import BeautifulSoup
#req=urllib2.urlopen("https://www.zhihu.com/topic")
'''
browser=webdriver.Chrome()
try:
    browser.get("https://www.zhihu.com/topic")
    time.sleep(2)
    print browser.page_source
    browser.close()
except UnicodeError:
    browser.close()
'''
header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
'Connection':'Keep-Alive',
}
#page=urllib.urlopen("https://www.zhihu.com/people/suan-le-ba/answers",None,header).read()
#print page
file=open('E:\zhihu/zhihuUser.html','r+').read()
'''
soup=BeautifulSoup(file,"lxml")
print '关注他的人数量'
care = soup.find_all('div', class_='NumberBoard-value')
#for y in care:
print care[1]
'''
#cares=care[1]
care_num=re.findall(r'<div class="NumberBoard-value">\d+',file)
#print care_num
#print r'感谢数和收藏数'
#good=soup.find_all('div',class_='Profile-sideColumnItemValue')
#print good[1]
user_name=''
agree_num=re.findall(r'获得 \d+ 次赞同',file)
thank_num=re.findall(r'获得 \d+ 次感谢',file)
collection_num=re.findall(r'\d+ 次收藏',file)
print '感谢数:'
print re.split(' ',thank_num[0])[1]
print '收藏数:'
print re.split(' ',collection_num[0])[0]
print '赞同数:'
print re.split(' ',agree_num[0])[1]
print '关注他的人：'
print re.sub(r'\D','',care_num[1])
#for x in se:
    #ok=re.split(' ',x[1])
    #print ok[1]
