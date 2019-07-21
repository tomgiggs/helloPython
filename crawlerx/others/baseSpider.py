# encoding=utf8
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
import pymongo
from multiprocessing import process
from threading import Thread




class BaseSpider(object):

    def __init__(self, *kw):
        self.processor = None
        self.store_func = None
        self.header = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "1"
        }
        self.base_url = kw.url
        self.httpClient = requests.session()
        if "processor" in kw:
            self.processor = kw["processor"]
        if "store_func":
            self.store_func = kw["store_func"]
        self.resp_count = 0
        self.output_file = None
        self.user_agents = json.loads(open('./useragents.json').read())
        self.db_client = None

    def setHeader(self, headers):
        self.header = headers

    def clean_data(self, body):
        if body:
            cleanData = " ".join(body).replace("\n", "").replace("\t", "").replace(" ", "")
        else:
            cleanData = ""
        return cleanData

    def request_page(self):
        while True:
            request_data_generator = self.gen_task()
            request_data = request_data_generator.next()
            if not request_data:
                print("job done,exiting.....")
                return
            agent = random.choice(self.user_agents['browsers']['chrome'])
            self.header['User-Agent'] = agent
            resp_data = self.httpClient.request(method=request_data["method"], url=request_data["url"], headers=self.header)
            data = self.process_body(resp_data) #处理后的数据应该是一个字典
            self.store_result(data)

    def htmlParser(self,page):
        html = etree.HTML(page.text)
        return html

    def write_file(self, data):
        try:
            if not self.output_file:
                self.output_file = open('spider_data_' + str(self.resp_count), 'a+', encoding='utf8')

            self.output_file.writelines(json.dumps(data))
            self.resp_count += 1
            if self.resp_count % 400 == 0:
                self.output_file.close()
                self.output_file = open('spider_data_' + str(self.resp_count), 'a+', encoding='utf8')
        except:
            traceback.print_exc()

    def process_body(self, body):
        if not self.processor:
            return body
        if self.processor and isinstance(self.processor, types.FunctionType):
            return self.processor(body)

    def store_result(self, data):
        if not self.store_func(data):
            self.write_file(data)
        if self.store_func and isinstance(self.store_func, types.FunctionType):
            self.store_func(data)

    def gen_task(self, start=0, end=100):
        for i in range(start, end):
            yield {
                "method":"get",
                "url":""
            }

    def init_db_client(self,db_name):
        if db_name=="mongo":
            mongo_config = {'host': '127.0.0.1','port': 27017,'db': 'netease_music',}
            try:
                self.db_client = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])
            except Exception:
                print(traceback.format_exc())
        if db_name == "mysql":
            self.db_client



    def multiProcess(self, thread_num, begin):
        pass
        # for i in range(thread_num):
        #     t = Thread(target=start, name=i, args=(begin,begin+100000))
        #     t.start()
        #     begin += 100000
