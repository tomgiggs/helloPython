#encoding=utf8
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import json
import csv
import time
import traceback
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import logging
import jieba

query_param = {
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "proj_name": "水利"
          }
        },
        {
          "term": {
            "proj_name": "工程"
          }
        }
      ],
      "must_not": [],
      "should": [
        {
          "term": {
            "proj_name": "高速"
          }
        }
      ]
    }
  },
  "from": 0,
  "size": 20,
  "_source": [
    "proj_app",
    "build_address",
    "proj_name"],
  "sort": [
    {
      "total_investment": {
        "order": "desc"
      }
    }
  ]
}
es = Elasticsearch('localhost:9200')


def search():
    result = es.search(index='exmaple',body=query_param)
    records = result['hits']


def cutword():
    raw_str = '大理州国家储备林建设洱海流域生态质量提升一期工程项目'
    itr = jieba.cut(raw_str, cut_all=True)
    words = jieba.cut_for_search(raw_str)
    print(','.join(words))

    for record in itr:
        print(record)
        pass

    pass
cutword()


# search()
