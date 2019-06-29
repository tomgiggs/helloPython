#encoding=utf8
"""
爬虫基类，主要用于有规律可循的网页爬取（请求可以按数值递增），支持多进程/多线程，支持多种HTTP操作，支持传入解析器函数进行网页解析，支持传入消息保存函数进行信息存储，最基本的消息写出方式是写文件。

"""
import json
import os
import types
import time
import traceback
from lxml import etree
import requests
import random
from multiprocessing import process
from threading import Thread
user_agents = json.loads(open('crawlerx/useragents.json').read())

class BaseSpider(object):
    def __init__(self,*kw):
        self.header = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "1"
        }
        self.base_url = kw.url


    def clean_data(self,body):
        if body:
            cleanData = " ".join(body).replace("\n", "").replace("\t", "").replace(" ", "")
        else:
            cleanData = ""
        return cleanData

    def request_get(self,start_index,end_index):
        httpClient = requests.session()

        file_out = open('pengpai_news_'+str(start_index), 'a+', encoding='utf8')
        agent = ""
        for i in range(start_index,end_index):
            agent = random.choice(user_agents['browsers']['chrome'])
            self.header['User-Agent'] = agent
            try:
                url = 'https://www.thepaper.cn/newsDetail_forward_'+str(i)

            except Exception as e:
                traceback.print_exc()
                time.sleep(10)
                pass
            time.sleep(0.01)
        file_out.close()
    def request_post(self):

        pass


    def process_body(self,body,func=None):
        if not func:
            return body
        if func and isinstance(func, types.FunctionType):
            return func(body)

    def store_result(self,data,func=None):

        pass

    def multiProcess(self,thread_num,begin):
        pass
        # for i in range(thread_num):
        #     t = Thread(target=start, name=i, args=(begin,begin+100000))
        #     t.start()
        #     begin += 100000


