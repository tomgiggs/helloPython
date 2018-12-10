#encoding=utf8
# import urllib2
import urllib
import hashlib
import requests

'''
使用requests下载文件或者图片
'''
def downloadfile():
    client = requests.session()
    url = 'https://github.com/longwosion/geojson-map-china/blob/master/china.json'
    filebody = client.get(url, stream=True)
    content = filebody.content
    out = open("geochiina.json", 'ab+')
    out.write(content)
    out.close()
    client.close()

downloadfile()
'''
使用urllib2 下载图片或者文件
'''
def downloadv2():
    #这个头部可以从浏览器复制过来,然后修改掉cookie还有其他验证信息就好
    header = {
        "User-Agent": " Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; ZTE C880U Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
        'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
        }
    url = "http://ipad-cms.csdn.net/cms/attachment/201705/58fef29fb7512.png"
    # request = urllib2.Request(url, headers=header)
    # image = urllib2.urlopen(request).read()
    file = open('./img_demo.png', "wb+")
    # file.write(image)
    file.flush()
    file.close()
    #这个可以直接下载，省去上面的繁琐
    # path = "e:\photo/123.png"
    # urllib.urlretrieve(url, path)


#获取地理位置信息
def gen_url(location_info):
    queryStr = '/geocoder/v2/?address='+location_info+'+&output=json&ak=A7mGEhDp4ROX7IfBEzIqlAYyQ9GdA5V9'
    encodedStr = urllib.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上yoursk
    rawStr = encodedStr + 'xxx'
    hashed = hashlib.md5(urllib.quote_plus(rawStr)).hexdigest()
    return 'http://api.map.baidu.com'+encodedStr+'&sn='+hashed

# print( gen_url('福建省福州市东方百货'))