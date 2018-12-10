# coding: utf-8

import json
from scrapy_redis.spiders import RedisSpider
from scrapy import Item, Field

class ShopeeBuyerSpider(RedisSpider):
    name = 'shopee_good'
    redis_key = 'shopee_good:start_urls'
    allowed_domains = ['shopee.com.my', 'shopee.sg', 'shopee.co.id', 'shopee.co.th', 'shopee.vn', 'shopee.ph']

    custom_settings = {
        'CONCURRENT_REQUESTS': 300,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 300,
        'ITEM_PIPELINES': {
            'crawlerx.pipelines.MongoPipeline': 100,
        }
    }

    def parse(self, response):
        yield response.body
