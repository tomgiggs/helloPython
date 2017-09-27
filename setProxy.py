import re
import urllib
import urllib2
import random
'''
url='https://www.zhihu.com/people/lu-chen-xi-9-98/activities'
header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
'Connection':'Keep-Alive',
}

request=urllib.urlopen(url,'112.217.228.212:8080',header).read()
print request.decode('utf-8')
'''

proxies=['80.107.117.210:3128','93.91.112.185:80','158.140.175.104:8080']
x=random.randint(0,2)
print x

proxy_handler = urllib2.ProxyHandler({'http': x})
opener = urllib2.build_opener(proxy_handler)
r = opener.open('https://www.zhihu.com/people/lu-chen-xi-9-98/activities')
print(r.read())
