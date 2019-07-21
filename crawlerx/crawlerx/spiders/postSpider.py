# coding: utf-8
'''
获取存在redis的数据，解析后发送post请求
'''
import json
import six
from scrapy import Item, Field,Spider,Request
from baseformspider import BaseFormRequest
from scrapy_redis import defaults
from scrapy_redis.spiders import RedisSpider


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s

class PostSpider(RedisSpider):
    name = 'postspider'
    start_urls = ['http://127.0.0.1:5555/api/users']
    def next_requests(self):

        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        found = 0
        # TODO: Use redis pipeline execution.
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            print data
            task_data = json.loads(data)
            task_url = task_data['url']
            url = bytes_to_str(task_url, self.redis_encoding)
            headers = {
                'Content-Type': 'application/json'
            }
            req = Request(url, method = 'POST', headers = headers, body=json.dumps(task_data["formdata"]), callback = self.parse, dont_filter = True)
            req.extra_data = task_data
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)


    def start_requests(self):
        return self.next_requests()
        # url = 'http://127.0.0.1:5555/api/users'
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # data ={"username":"sss","password":"hahahah"}
        # # yield BaseFormRequest(url, method = 'POST', headers = headers, formdata=data, callback = self.parse, dont_filter = True)
        # yield Request(url, method = 'POST', headers = headers, body=json.dumps(data), callback = self.parse, dont_filter = True)#直接使用scrapy发送post请求

    def parse(self, response):
        print response
        print response.body


