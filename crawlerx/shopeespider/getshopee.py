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
    print( traceback.format_exc())
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
    infotable = db.product_info
    infotable.insert(record['data'])



def get_state_timely():
    for i in range(44391600, 44396417):
        start_url = 'https://shopee.com.my/api/v2/shop/get?is_brief=1&shopid=' + str(i)
        body = requests.get(start_url)
        try:
            record = json.loads(body.text)
        except:
            continue
        if 'data' in record and record['data']:
            insert_to_mongodb_formal(record)
        time.sleep(0.05)

if __name__ == "__main__":
    get_state_timely()
