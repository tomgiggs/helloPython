# encoding=utf8
import json
import os
import time
import requests
from multiprocessing import process
from threading import Thread
import execjs
# url = 'http://192.168.19.55:9200/vr_mmo_product_set_info_qa_20190524_ik001/_search'
url = 'http://192.168.19.55:9200/vr_mmo_product_set_info_qa_20190524/_search'
header = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Origin": "chrome-extension://aejoelaoggembcahagimdiliamlcdmfm",
    "Cache-Control": "no-cache",
}
body = '''
{
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "must": [
              {
                "match_phrase": {
                  "productname": "跑酷"
                }
              }
            ]
          }
        }
      ],
      "must_not": []
    }
  },
  "from": 0,
  "size": 12,
  "sort": []
}
'''


wildcard = '''
{
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "must": [
              {
                "wildcard": {
                  "productname": "*水果*"
                }
              }
            ]
          }
        }
      ],
      "must_not": []
    }
  },
  "from": 0,
  "size": 12,
  "sort": []
}
'''
match100m = '''
{
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "must": [
              {
                "match": {
                  "productname": "水果"
                }
              }
            ]
          }
        }
      ],
      "must_not": []
    }
  },
  "from": 0,
  "size": 12,
  "sort": []
}
'''
match10k = '''
{
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "must": [
              {
                "match_phrase": {
                  "productname": "大河"
                }
              }
            ]
          }
        }
      ],
      "must_not": []
    }
  },
  "from": 0,
  "size": 12,
  "sort": []
}
'''

match100k = '''
{
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "must": [
              {
                "match_phrase": {
                  "productname": "奖金"
                }
              }
            ]
          }
        }
      ],
      "must_not": []
    }
  },
  "from": 0,
  "size": 12,
  "sort": []
}
'''

times = 20
min_cost = 0
max_cost = 0
threadNum = 2
count = 1
totalCost = 0
stopNum = 0


def process():
    httpClient = requests.session()

    global stopNum
    global totalCost
    global count
    global min_cost
    global max_cost
    while count < times:
        # for i in range(1, times):
        begin = time.time()
        # result = httpClient.post(url, body.encode('utf-8'), headers=header)
        result = httpClient.post(url, wildcard.encode('utf-8'), headers=header)
        # result = httpClient.post(url, match100k.encode('utf-8'), headers=header)
        # result = httpClient.post(url, match10k.encode('utf-8'), headers=header)
        # result = httpClient.post(url, match100m.encode('utf-8'), headers=header)
        # print(result.text)
        cost = time.time() - begin
        totalCost += cost
        # totalCost = totalCost +cost
        if cost > max_cost:
            max_cost = cost
        if cost < min_cost:
            min_cost = cost
        if count == 1:
            min_cost = cost
        print(totalCost / count, min_cost, max_cost)
        count += 1
    stopNum += 1


def getQPS():
    while True:
        if stopNum == threadNum:
            print('qps is:', count / totalCost)
            break
    time.sleep(1)


def multiProcess():
    for i in range(threadNum):
        t = Thread(target=process, name=i, args=())
        t.start()
    Thread(target=getQPS, name=i, args=()).start()


# multiProcess()

productnameList = ['排名', '成绩', '云计算服务', '数据库', '程序员',
            '产品', '模型', '社区项目', 'Google', '核心小团队', '微软', '疾驰', 'Go社区']
import random
print(random.choice(productnameList))

