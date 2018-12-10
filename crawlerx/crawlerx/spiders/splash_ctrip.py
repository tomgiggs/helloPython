# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Item
from scrapy_splash.request import SplashRequest
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from scrapy_redis import defaults
import json
import six
import scrapy_splash

def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s

class SplashCtripSpider(RedisSpider):
    name = 'splash_ctrip'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://ctrip.com/']
    '''
    override RedisSpider method,get json task from redis
    '''
    def next_requests(self):
        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        # TODO: Use redis pipeline execution.
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            task_data = json.load(data)
            task_url = task_data['url']
            url = bytes_to_str(task_url, self.redis_encoding)
            # req = Request(url, dont_filter=True)
            req = SplashRequest(url, self.parse_result,
                                args={
                                    # optional; parameters passed to Splash HTTP API
                                    'wait': 0.5,

                                    # 'url' is prefilled from request url
                                    # 'http_method' is set to 'POST' for POST requests
                                    # 'body' is set to request body for POST requests
                                },
                                endpoint='render.json',  # optional; default is render.html
                                splash_url='<url>',  # optional; overrides SPLASH_URL
                                slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                )
            '''
            the second method to use SplashRequest
            '''
            # req = scrapy.Request(url, self.parse_result, meta={
            #     'splash': {
            #         'args': {
            #             # set rendering arguments here
            #             'html': 1,
            #             'png': 1,
            #
            #             # 'url' is prefilled from request url
            #             # 'http_method' is set to 'POST' for POST requests
            #             # 'body' is set to request body for POST requests
            #         },
            #
            #         # optional parameters
            #         'endpoint': 'render.json',  # optional; default is render.json
            #         'splash_url': '<url>',  # optional; overrides SPLASH_URL
            #         'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
            #         'splash_headers': {},  # optional; a dict with headers sent to Splash
            #         'dont_process_response': True,  # optional, default is False
            #         'dont_send_headers': True,  # optional, default is False
            #         'magic_response': False,  # optional, default is True
            #     }
            # })
            req.extra_data = task_data
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)


    def start_requests(self):
            self.next_requests()


    def parse(self, response):
        pass
