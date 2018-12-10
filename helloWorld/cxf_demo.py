# encoding=utf8
import os
import sys
import requests
# import suds
# from suds import WebFault
from suds.client import Client

def testsuds():
    # url = 'http://127.0.0.1:8787/Entrance?wsdl'
    # url = 'http://127.0.0.1:8787/FileService?wsdl'
    urlx = 'http://www.webxml.com.cn/webservices/qqOnlineWebService.asmx?wsdl'
    client = Client(urlx)
    print(client)
    # print(client.service) #报错MethodNotFound: Method not found: 'FileServiceImpService.FileServiceImpPort.__str__'，
    # 但是java调用是成功的,用QQ的接口测也失败了，不知道为什么，client.service每次只能调用一次，不能重复调用，不然会报错
    '''
    原因是每次client.service 不能直接调用，必须加上具体的服务
    '''
    print(client.service.qqCheckOnline("1369796093"))
testsuds()