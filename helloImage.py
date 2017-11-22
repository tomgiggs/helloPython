import re
import urllib2
import urllib
import  requests
import  socket
photoUrl=""
path="E:\photo/"
header = {"User-Agent":" Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",

    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive'
}

for x in range(265,285):
        for p in range(x*100+5,x*100+9):
            for y in range(1,10):

                    filepath=path+str(p)+str(y)+".jpg"
                    photo = photoUrl+str(x)+"/"+str(p)+"-"+str(y)+".jpg"
                    print photo
                    request=urllib2.Request(photo,headers=header)
                    image=urllib2.urlopen(request).read()

                    #print image
                    file = open(filepath, "wb+")

                    file.write(image)
                    file.flush()
                    file.close()

'''
                    #
                    #page=urllib.urlopen(photo)
                    page=requests.get(photo,timeout=10)
                    
'''



