import urllib
from StringIO import StringIO
import gzip
import urllib2
import logging

user_agent="Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) UC AppleWebKit/534.31 (KHTML, like Gecko) Mobile Safari/534.31"
header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
'Connection':'Keep-Alive',
}


#req=urllib2.Request("https://www.zhihu.com/topic",headers)
#urlpath="https://zhuanlan.zhihu.com/p/"
urlpath="https://www.zhihu.com/question/"
path="E:/hesult2/"
for x in range(28100000,28100050):
    url=urlpath+str(x)
    req=urllib.urlopen(url,None,header)
    filex=path+str(x)+".txt"
    file=open(filex,"w+")
    file.write(req.read())
    file.close()

#req=urllib.urlopen("https://zhuanlan.zhihu.com/p/28741493",None,header)

#file=open("E:\hesult\hello.txt","w+")
#file.write(req.read())
#print req.read()