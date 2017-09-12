import cookielib
import urllib2
filename="D:\cookie.txt"
cookie=cookielib.MozillaCookieJar(filename)

handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)
respone=opener.open("https://www.zhihu.com/")
cookie.save()