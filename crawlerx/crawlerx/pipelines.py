# -*- coding: utf-8 -*-
import sys
# reload(sys)
sys.setdefaultencoding('utf-8')
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
# import MySQLdb 这个在Python3版本不再可用，改成pymysql
import pymongo
import pymysql
# from scrapy_redis.spiders import RedisSpider
import datetime
import  sys
import traceback
# from scrapy.utils.project import inside_project, get_project_settings
# from scrapy_redis import connection, defaults
# from scrapy_redis.pipelines import RedisPipeline
# #import pymysql


class MongoPipeline(object):

    def process_item(self, item, spider):

        self.insertToMongo(item)
        return item

    def insertToMongo(self, item):
        mongo_config = {
            'host': '127.0.0.1',
            'port': 27017,
            'db': 'product_info',
            # 'username': 'root',
            # 'password': 'root',
        }
        try:
            conn = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])
            db = conn[mongo_config['db']]
            # username = mongo_config['username']
            # password = mongo_config['password']
            # if username and password:
            #     db.authenticate(username, password)
        except Exception:
            print(traceback.format_exc())
        infotable = db.info
        infotable.insert(dict(item))

class CrawlerxPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def process_item(self, item, spider):

        self.insertToMysql(item)
        return item

    def insertToMysql(self, item):
        try:
            conn = pymysql.connect(host='localhost', user='root', passwd='root', db='zhihu_info', port=3306)
            cur = conn.cursor()
        except:
            print(traceback.print_exc())
            return
        try:
            sql = "insert into user(name,care_num,agree_num,thank_num,collection_num)values('%s',%s,%s,%s,%s)" % (
            item['xx'], item['aa'], item['bb'], item['cc'], item['dd'])
            cur.execute(sql)
            cur.close()
            conn.close()

        except:
            cur.close()
            conn.close()
class SSDBPipeline(object):
    def process_item(self, item, spider):

        self.insertToSSDB(item)
        return item
    def insertToSSDB(self,item):
        pass

class RedisPipeline(object):
    def process_itme(self,item,spider):
        pass


class PostgresqlPipeline(object):
    def process_itme(self,item,spider):
        pass

class KafkaPipeline(object):

    def process_itme(self,item,spider):
        pass



