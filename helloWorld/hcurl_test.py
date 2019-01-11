import human_curl
from human_curl.async import AsyncClient


def success_call_back(**kw):
    # kw = {'async_client': <human_curl.async.AsyncClient object at 0x000000000380C9E8>, 'opener': <pycurl.Curl object at 0x000000000383C778>, 'response': <Response: 200 >}
    print(kw)
    if kw.has_key('async_client'):
        print(kw['async_client'])
        client = kw['async_client']
        print(client)
    if kw.has_key('response'):
        print(kw['response'].headers)
        print(kw['response'].content)

    print("success")
    pass


def fail_call_back(**kw):
    print('failed')
    pass


client = AsyncClient(success_callback=success_call_back, fail_callback=fail_call_back)
# client.get('https://github.com/lispython/human_curl',)

# client.start()
# client.get('https://blog.csdn.net/wjskeepmaking/article/details/64905745')
# client.method(**{'method':'get', 'url':'https://blog.csdn.net/wjskeepmaking/article/details/64905745'})
client.method(**{'method': 'post', 'url': 'https://sellercentral.amazon.com/fba/profitabilitycalculator/getafnfee',
                 'data': '{"productInfoMapping":{"asin":"B06W9KM4WG","dimensionUnit": "inches","encryptedMarketplaceId": "","subCategory": "","weight": 1.25,"title": "BEXEL Super Alkaline AA Batteries 24 PACK","weightUnit": "pounds", "isWhiteGloveRequired": false,"imageUrl": "https://images-na.ssl-images-amazon.com/images/I/21qMWE048eL._SCLZZZZZZZ__SL120_.jpg","binding": "consumer_electronics","productGroup": "","height": 3.4646,"thumbStringUrl": "https://images-na.ssl-images-amazon.com/images/I/21qMWE048eL._SCLZZZZZZZ__SL80_.jpg","width": 2.3622,"length": 1.9685,"originalUrl": "", "link": "http://www.amazon.com/gp/product/B06W9KM4WG/ref=silver_xx_cont_revecalc", "dimensionUnitString": "inches", "gl": "gl_electronics", "isAsinLimits": true, "weightUnitString": "pounds"},"afnPriceStr":7.25,"mfnPriceStr":0,"mfnShippingPriceStr":0,"currency":"USD","marketPlaceId":"ATVPDKIKX0DER","hasFutureFee":false,"futureFeeDate":"2018-02-25 00:00:00","hasTaxPage":true} ',
                 'headers': {'Content-Type': 'application/json;charset=UTF-8',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
                             }

                 })

client.start()
# import json
#
# html = human_curl.post('https://sellercentral.amazon.com/fba/profitabilitycalculator/getafnfee?profitcalcToken=CdKo3CQuKab1GdSryuP6CZYj2F0Jgj3D',data=json.dumps(
# {"productInfoMapping": {"asin": "B06W9KM4WG", "dimensionUnit": "inches",
#                                                                  "encryptedMarketplaceId": "", "subCategory": "", "weight": 1.25,
#                                                                  "title": "BEXEL Super Alkaline AA Batteries 24 PACK",
#                                                                  "weightUnit": "pounds", "isWhiteGloveRequired": False,
#                                                                  "imageUrl": "https://images-na.ssl-images-amazon.com/images/I/21qMWE048eL._SCLZZZZZZZ__SL120_.jpg",
#                                                                  "binding": "consumer_electronics", "productGroup": "",
#                                                                  "height": 3.4646,
#                                                                  "thumbStringUrl": "https://images-na.ssl-images-amazon.com/images/I/21qMWE048eL._SCLZZZZZZZ__SL80_.jpg",
#                                                                  "width": 2.3622, "length": 1.9685, "originalUrl": "",
#                                                                  "link": "http://www.amazon.com/gp/product/B06W9KM4WG/ref=silver_xx_cont_revecalc",
#                                                                  "dimensionUnitString": "inches", "gl": "gl_electronics",
#                                                                  "isAsinLimits": True, "weightUnitString": "pounds"},
#                                           "afnPriceStr": 7.25, "mfnPriceStr": 0, "mfnShippingPriceStr": 0, "currency": "USD",
#                                           "marketPlaceId": "ATVPDKIKX0DER", "hasFutureFee": False,
#                                           "futureFeeDate": "2018-02-25 00:00:00", "hasTaxPage": True}),
#                        headers={
#                            'Content-Type': 'application/json;charset=UTF-8',
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
#                            'cookie':'aws-ubid-main=418-3562340-7064756; aws-account-alias=zixun; regStatus=registered; aws-target-static-id=1519804009977-42094; aws-target-data=%7B%22support%22%3A%221%22%7D; sst-main=Sst1|PQERqvlx25TOrwhKmm46XOfuC1w1tYXp_Hx47Mn46Bt9IqVP7JMk3HjfrghA_SoK2RnTbWoRyRgn45nfFvcC0ne1aHBsQQjlBDzYOpeo4IEqwWTrsAGN7drEVmghvTrpdV9mU2c-EZEmR-TrBqh73VF5M24gn3VEwYgXLfJtkRyt549HpVPTIhfWCCcGJR-A5t_lzJnfSQKTK9rPnCXplYO5twhGtHjknsaO8oMlD_1WKSic2vYzyzsm-IKEzZ5Oc6JwPFkB5XdP2pLptGGWnC_DsGjN3QPjNetQ82_ujW6C6DfLYe_llgYythyH7L31sL1pjSBvXY2qO1x5CLRvF-gtgg; x-wl-uid=1jHyCh5savvlLNECq8bspJ2ArFKUYtnjo1KgyFVb8psZAab1EYRXYG1pV+PRsPr5SJyKhkj1cZnGRw26+b/efA3DHr6wBB8/d1TO2mlwHPMOE7gedRH/qVxrmWcVDT2BhzTt17XwoT5U=; s_pers=%20s_fid%3D2B59D6EA9259D485-2F919BE274C93981%7C1681702883137%3B%20s_ev15%3D%255B%255B%2527Typed/Bookmarked%2527%252C%25271523182057859%2527%255D%252C%255B%2527Typed/Bookmarked%2527%252C%25271523927909549%2527%255D%252C%255B%2527SCFBAStriplogin%2527%252C%25271523936483170%2527%255D%252C%255B%2527Typed/Bookmarked%2527%252C%25271523944513435%2527%255D%252C%255B%2527Typed/Bookmarked%2527%252C%25271523948018478%2527%255D%252C%255B%2527Typed/Bookmarked%2527%252C%25271523948020268%2527%255D%252C%255B%2527Typed/Bookmarked%2527%252C%25271523948025582%2527%255D%252C%255B%2527Typed/Bookmarked%2527%252C%25271523948025952%2527%255D%252C%255B%2527Typed/Bookmarked%2527%252C%25271523948028322%2527%255D%255D%7C1681714428322%3B%20s_dl%3D1%7C1523950536129%3B%20gpv_page%3DUS%253ASC%253A%2520SellerCentralLogin%7C1523950536137%3B; s_fid=20BA153E7B22B435-12A62D0141554AFC; session-id-time=2082787201l; __utma=194891197.597643680.1521441040.1526016790.1527164120.66; __utmz=194891197.1527164120.66.11.utmccn=(referral)|utmcsr=us-east-2.console.aws.amazon.com|utmcct=/athena/home|utmcmd=referral; skin=noskin; s_cc=true; s_vnum=1951872289901%26vn%3D2; s_sq=%5B%5BB%5D%5D; s_ppv=100; aws-mkto-trk=id%3A112-TZM-766%26token%3A_mch-aws.amazon.com-1521550962598-63363; aws_lang=cn; s_vn=1552544598301%26vn%3D20; aws-target-visitor-id=1519804009982-764131.28_15; s_dslv=1530174008258; s_nr=1530174008261-Repeat; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A113706105081%3Auser%2Fyilong_chen%40ziguangcn.com%22%2C%22alias%22%3A%22zixun%22%2C%22username%22%3A%22yilong_chen%40ziguangcn.com%22%2C%22keybase%22%3A%228ZWjZVR3BRDQWmKjTqzX4lvwkL6Lzh0nvo4piP7Ffwc%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%7D; session-id=130-2910729-6008820; ubid-main=135-0349568-1664157; session-token="kjzAFyT7O4S0gNPDDqcnhMIdVKbroARdJbZr2QFPU7cl1Jm5VTLNS3OXEbnDs2IF6AHvoVsKSM8pBP78E81osFZ7bHeY4JRUx6OH1NLyjOPuI1DlF3dwskusActP93JzBuJcRo3WrMO13otAYSj1oq+3gyJ/vb/LF0VnZmldObDexK4kmTHzpgRw4CuqvK9iTBshua4sdjvTNg3AitkL4A=="; csm-hit=tb:RYZ0K45WZJV83KKBVCY7+s-PPRNFZ5YDYV12QSW6PY8|1530693418131&adb:adblk_no'
# }
#                 )
# print(html)
# encoding=utf8
import struct
import socket
import human_curl
from human_curl.async import AsyncClient
from human_curl.core import Request
import pycurl
import socket

# import fcntl
# print(struct.pack('i',25))
# print("eth0:5"[:15])
# print(struct.pack('256s', "185.101.107.122"))
# print bin(ord('s'))
#
#
# ipstr = (fcntl.ioctl( s.fileno(),  0x8915,  struct.pack('256s', "eth0:5"))[20:24])
# print([bin(ord(x)) for x in ipstr])

# 将ip地址转化为整数，然后将整数转为ip
packedip = socket.inet_aton('185.101.107.122')
print(struct.unpack('!L', packedip))
print(socket.inet_ntoa(struct.pack('!L', 3110431610L)))


def success_call(response, **kwargs):
    print(response.content)



def fail_call(response, **kwargs):
    print(response.content)


def get_ip():
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    print(ip)


# get_ip()

url = 'https://blog.csdn.net/fly_zhyu/article/details/76408158'
client = AsyncClient(success_callback=success_call, fail_callback=fail_call)
# request = Request(network_interface='185.101.107.106',method='GET', url=url)
# print(request.response)
# request.send()
# response = request.response
# print(response.content)
# print(request.make_response())
# request._network_interface='172.17.35.241'
# #
# opener = pycurl.Curl()
da = {'network_interface': 'eth0:5', }
da = {'network_interface': '185.101.107.122', }
client.add_handler(**da)
# client.configure_opener(opener, data=da)
client.get(url)
client.start()


# import lz4
# # egg: http://python-lz4.readthedocs.io/en/stable/quickstart.html#simple-usage
# compressed = lz4.frame.compress('10111001110010111010111111010')
# decompressed = lz4.frame.decompress(compressed)
# print(decompressed)