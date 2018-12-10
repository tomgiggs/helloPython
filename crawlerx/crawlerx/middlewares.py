# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import json
import redis
import time
import settings

f_user_agent = open('./useragents.json', 'r')
user_agent_list = []
agents = json.loads(f_user_agent.read())
browsers = agents['browsers']
for key in browsers:
    for user_agent in browsers[key]:
        user_agent_list.append(user_agent)
f_user_agent.close()


class CrawlerxSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self):
        """Initialize middleware"""
        f_proxy = open('./proxies.txt', 'r')
        self.proxy_list = []
        for line in f_proxy.readlines():
            self.proxy_list.append(line.strip())
        f_proxy.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def process_request(self, request, spider):
        if len(self.proxy_list) > 0:
            request.meta['proxy'] = random.choice(self.proxy_list)
            print request.meta['proxy']
        request.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        request.headers['Accept-Encoding'] = 'gzip, deflate'
        request.headers['User-Agent'] = random.choice(user_agent_list)

    def process_response(self, request, response, spider):
        if request.task:
            response.task = request.task
        return response

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class CrawlerxDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class CheckFailMiddleware(object):
    """通过response判断任务是否失败，需要在retrymiddleware之后拦截"""

    def process_response(self, request, response, spider):
        if response.status == 200 or response.status == 201:
            if response.body is None:
                # 可能遭到反爬,推送到失败队列处理
                spider.request_failed(request, response)
        elif response.status == 404:
            # 404有可能是该node本身是空页面，不视为失败任务
            return response
        else:
            spider.request_failed(request, response)

        return response
