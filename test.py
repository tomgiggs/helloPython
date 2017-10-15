
import  redis
import urllib
import logging
'''
zhihu = redis.Redis(host="127.0.0.1", port=6379, db=0)
usr=zhihu.smembers('urls')
print usr

file=open('E:/usr.txt','w+')
for x in usr:
    file.write(x)

    file.write('\n')
file.close()
'''
header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
'Connection':'Keep-Alive',
}
#page=urllib.urlopen('https://www.zhihu.com/people/xiao-ai-gua-15-55/activities',None,header).read()
#print page

#logging.error('this is a info')




