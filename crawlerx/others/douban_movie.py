# encoding=utf8
import pymongo
import requests
import traceback
import time
import redis
import json
import json
import random

# rclient = redis.Redis('127.0.0.1', 6379)
client = requests.session()

mongo_config = {
    'host': '127.0.0.1',
    'port': 27017,
    'db': 'movie_reviews',
}

try:
    conn = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])
    db = conn[mongo_config['db']]
except Exception:
    print(traceback.format_exc())
    exit(-1)


def insert_to_mongodb_formal(record):
    infotable = db.movie_reviews
    infotable.insert(record)


topic_no = ['108','54','254','234896','5445','82734','3220','50723','396236','180877','27673','1658','6488','8278','610401','14905','101727','4989','176','7054','3784','395040','11959','1740','327','1728','188450','115','20190','209','35','124','101','88','413','5699','5968','15','54','13','108','54','254','234896','5445','82734','3220','50723','396236','180877']

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "m.douban.com",
    "Origin": "https://www.douban.com",
    "Referer": "https://www.douban.com/gallery/topic/39611/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    'Cookie': 'bid=o7hqHo0Ihng; douban-fav-remind=1; ll="118348"; __utmz=30149280.1541170013.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=D26CEFB989AE1E2D6AD65CA7448F97678|2b0bf511910df757d1361aa1fc353857; __utma=30149280.322464962.1534051988.1541170013.1547111381.5; __utmc=30149280; ap_v=0,6.0; __utmt=1; __utmb=30149280.1.10.1547111381'
}

client.headers.update(headers)


def get_data():
    for no in topic_no:
        preurl = 'https://m.douban.com/rexxar/api/v2/gallery/topic/$$$/items?sort=hot&start=0&count=20&status_full_text=1&guest_only=0&ck=null'
        body = client.get(preurl.replace('$$$',no))
        record = json.loads(body.text)
        insert_to_mongodb_formal(record)

get_data()