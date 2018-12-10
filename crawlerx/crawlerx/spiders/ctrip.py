# -*- coding: utf-8 -*-
from scrapy import Spider,Item
from scrapy import Item,Spider,Field
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import bs4
import re
import json
from scrapy_redis.spiders import RedisSpider
from scrapy.utils.project import inside_project, get_project_settings
# from scrapy_redis import connection, defaults

# settings = get_project_settings()

class CtripSpider(RedisSpider):
    name = 'ctrip'
    allowed_domains = ['ctrip.com']
    start_urls = ['https://tuan.ctrip.com/group/hotel/city_Sanya/?sid=155952&allianceid=4897&ouid=table']

    count = 0
    name = 'ctrip'
    redis_key = 'ctrip:start_urls'
    start_urls = ['http://vacations.ctrip.com/whole-0B126DC258/?searchValue=%E5%91%A8%E8%BE%B9&searchText=%E5%91%A8%E8%BE%B9#ctm_ref=va_home_s258_lst3_ad1', ]
    # lpush ctrip:start_urls http://vacations.ctrip.com/whole-2A110000B126MO201809P8/?searchValue=%E5%91%A8%E8%BE%B9&searchText=%E5%91%A8%E8%BE%B9#_flta
    #allowed_domains = ['ctrip.com']
    #start_urls = ['http://ctrip.com/']


    def parse(self, response):
        self.count +=1
        items = response.xpath('//div[@class="main_mod product_box flag_product "]')
        page = bs4.BeautifulSoup(response.body,'lxml')
        first_text = page.find('textarea').get_text()
        main_text =PageInfoItem()
        main_text['all_info'] = first_text
        yield main_text
        for item in items:
            product_item = InfoItem()
            info = item.xpath('.//@data-tracevalue').extract_first()
            title = item.xpath('.//div[@class="product_main"]//h2//text()').extract_first()
            main_info = item.xpath('./textarea/text()').extract_first()
            # comments = item.xpath('.//div[@class="comment"]//a//text()').extract_first()
            # total_num = item.xpath('.//div[@class="comment"]//em//text()').extract_first()
            # price = item.xpath('.//div[@class="product_detuct"]//span[@class="sr_price"]//text()').extract_first()
            # product_schedule = item.xpath('.//div[@class="product_schedule"]//p//text()').extract_first()
            product_item['info'] = info
            product_item['title'] = title
            product_item['main_info'] = main_info

            print info,title
            yield product_item



    def get_num(self, raw_str):
        raw_str = self.replacechar(raw_str)
        if not raw_str:
            return 0
        num = 0
        try:
            num_rule = '[0-9]+[\.]?[0-9]*'
            comp_rule = re.compile(num_rule)
            raw_star = raw_str.replace(',', '')
            num = re.search(comp_rule, raw_star).group()
        except AttributeError:
            pass
        except:
            print traceback.print_exc()
            num = -1
        return num

    def getDomain(self, str):
        reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
        m = re.match(reg, str)
        uri = m.groups()[0] if m else ''
        domain = uri[uri.rfind('.', 0, uri.rfind('.')) + 1:]
        print domain
        domainLast = domain.find('.')
        country = domain[domainLast + 1:]
        if country == 'com':
            return 'us'
        return country

class InfoItem(Item):
    info = Field()
    title = Field()
    main_info = Field()

class PageInfoItem(Item):
    all_info = Field()
