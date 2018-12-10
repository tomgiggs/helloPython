# coding: utf-8
import redis
import random

url_path = "https://shopee.com.my/api/v2/shop/get?is_brief=1&shopid="
crawler_task_key = 'shopee_good:start_urls'

pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
r = redis.Redis(connection_pool=pool)

for i in range(44390000, 44396417):
    start_url = url_path+ str(i)
    r.rpush(crawler_task_key, start_url)
