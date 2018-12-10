# coding: utf-8

import json
from scrapy_redis.spiders import RedisSpider
from scrapy import Item, Field

class ShopeeBuyerSpider(RedisSpider):
    name = 'shopee_buyer'
    redis_key = 'shopee_buyer:start_urls'
    allowed_domains = ['shopee.com.my', 'shopee.sg', 'shopee.co.id', 'shopee.co.th', 'shopee.vn', 'shopee.ph']

    custom_settings = {
        'CONCURRENT_REQUESTS': 300,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 300,
        'ITEM_PIPELINES': {
            'crawlerx.pipelines.MongoPipeline': 100,
        }
    }

    def getContentByEnding(self, content, starting, ending):
        index = content.find(starting)
        result_str = ''
        if index > -1:
            result_str = content[index + len(starting):len(content)]
            index = result_str.find(ending)
            if index > -1:
                result_str = result_str[0:index]
        return result_str

    def getDomain(self, url):
        for domain in self.allowed_domains:
            if domain in url:
                return 'https://' + domain + '/'

    def parse(self, response):
        if response.status == 404:
            self.task_finished(response.request)
            return

        url = response.url
        buyer_id = self.getContentByEnding(url, 'buyer/', '/')
        shop_id = self.getContentByEnding(response.body, 'shopID = ', ';').strip()
        user_id = self.getContentByEnding(response.body, 'userID = ', ';').strip()

        if not shop_id or not user_id:
            self.enqueue_failed_task(response.request.task)
            self.task_finished(response.request)
            return

        buyer = BuyerItem()
        buyer['buyer_id'] = buyer_id
        buyer['shop_id'] = shop_id
        buyer['user_id'] = user_id
        yield buyer
        self.task_finished(response.request)

class BuyerItem(Item):
    shop_id = Field()
    buyer_id = Field()
    user_id = Field()
