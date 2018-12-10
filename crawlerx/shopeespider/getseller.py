# encoding=utf8
import pymongo
import requests
import traceback
import time
import redis
import json
import json
import random
import signal

rclient = redis.Redis('127.0.0.1',6379)
client = requests.session()
last_second = int(time.time())
i = 0

mongo_config = {
    'host': '127.0.0.1',
    'port': 27017,
    'db': 'shpopee',
}

try:
    conn = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])
    db = conn[mongo_config['db']]
except Exception:
    print(traceback.format_exc())
    print('Connect Database Fail.')
    exit(-1)

def exit_cleaner(signum, frame):
    try:
        conn.close()
        client.close()
    except:
        print(traceback.print_exc())
    exit(0)

signal.signal(signal.SIGINT, exit_cleaner)
signal.signal(signal.SIGTERM,exit_cleaner)


def insert_to_mongodb_formal(record):
    global last_second
    global i
    infotable = db.seller_info
    infotable.insert(record)



def get_state_timely():
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "ver": "v1.0",
        "clienttype": "web",
        "Referer": "http://wxv.zjkj888.cn/m/main/market",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "cezjv_think_language=zh-CN; cezjv=6l8un1mc61hl85gkjj6857m9c1",
    }
    url = 'http://wxv.zjkj888.cn/fiftyEtf/QryQuotationList'
    client.headers.update(headers)
    for i in range(821891, 822213):
    # for i in range(820000, 822213):
        start_url = 'https://shopee.com.my/api/v2/search_items/?by=pop&limit=30&match_id=xxxx&newest=0&order=desc&page_type=shop'.replace('xxxx',str(i))
        body = client.get(start_url)
        try:
            record = json.loads(body.text)
        except:
            continue
        if 'items' in record and record['items']:
            record['sellerid'] = i
            insert_to_mongodb_formal(record)
        time.sleep(0.02)

if __name__ == "__main__":
    get_state_timely()
