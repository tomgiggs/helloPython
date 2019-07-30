# encoding=utf8
from __future__ import with_statement

import flask
import redis
import json
import time
import os
from flask import Flask, session, jsonify, redirect, url_for, escape, request, g, config
from flask_restful import Resource, Api, abort
from flask_restful import reqparse
import signal
# import sys
# from imp import reload
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
import pymongo
import traceback
from flask_cors import *

app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
CORS(app, supports_credentials=True)

mongo_config = {
    'host': '127.0.0.1',
    'port': 27017,
    'db': 'stock_info',
}

try:
    conn = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])
    db = conn[mongo_config['db']]
except Exception:
    print(traceback.format_exc())
    print('Connect Database Fail.')
    exit(-1)

rclient = redis.Redis('127.0.0.1', 6379)

def exit_cleaner(signum, frame):
    try:
        conn.close()

    except:
        print(traceback.print_exc())
    exit(0)

signal.signal(signal.SIGINT, exit_cleaner)
signal.signal(signal.SIGTERM,exit_cleaner)


def make_resp(result):
    #在返回头添加跨域支持，头部不能包含中文字符串，只能是latin-1
    res = jsonify(result)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    res.headers['content-type'] = 'application/json;charset=utf-8'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res



def get_conncetion():
    global db
    return db

def scan_db(param):
    db = get_conncetion()
    result = []
    print(param)
    if 'gen_time_begin' not in param or 'gen_time_end' not in param:
        return
    try:
        condition_param = {"stock_code":param['stockid'],"gen_time":{"$gt":param['gen_time_begin'],"$lt":param['gen_time_end']}}
        for record in db.get_collection(param['tablename']).find(condition_param):
            result.append(record)
        return result
    except:
        print(traceback.print_exc())


def get_history_tag(param):
    db = get_conncetion()
    result = []
    print(param)
    if 'gen_time_begin' not in param or 'gen_time_end' not in param:
        return
    try:
        condition_param = {"tag_name":param['tag_name'],"gen_time":{"$gt":param['gen_time_begin'],"$lt":param['gen_time_end']}}
        for record in db.get_collection(param['tablename']).find(condition_param):
            result.append(record)
        return result
    except:
        print(traceback.print_exc())

class Recommend(Resource):

    def get(self, tag_name):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not tag_name:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            query_param['tag_name'] = tag_name
            query_param['tablename'] = 'stock_recomend'
            return make_resp(get_history_tag(query_param))
        else:
            result = rclient.hget('recomend_stock', tag_name)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}

class Sell(Resource):

    def get(self, tag_name):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not tag_name:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            query_param['tag_name'] = tag_name
            query_param['tablename'] = 'stock_sell'
            return make_resp(get_history_tag(query_param))
        else:
            result = rclient.hget('sell_stock', tag_name)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}

class Buy(Resource):

    def get(self, tag_name):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not tag_name:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            query_param['tag_name'] = tag_name
            query_param['tablename'] = 'stock_buy'
            return make_resp(get_history_tag(query_param))
        else:
            result = rclient.hget('buy_stock', tag_name)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}

class SellDetail(Resource):

    def get(self, tag_name):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not tag_name:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            query_param['tag_name'] = tag_name
            query_param['tablename'] = 'sell_detail'
            return make_resp(get_history_tag(query_param))
        else:
            result = rclient.hget('sell_detail', tag_name)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}

class RecommendDetail(Resource):

    def get(self, tag_name):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not tag_name:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            query_param['tag_name'] = tag_name
            query_param['tablename'] = 'recommend_detail'
            return make_resp(get_history_tag(query_param))
        else:
            result = rclient.hget('recommend_detail', tag_name)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}


class BuyDetail(Resource):

    def get(self, tag_name):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not tag_name:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            query_param['tag_name'] = tag_name
            query_param['tablename'] = 'buy_detail'
            return make_resp(get_history_tag(query_param))
        else:
            result = rclient.hget('buy_detail', tag_name)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}




class Five(Resource):

    def get(self, stockid):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not stockid:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            try:
                stockid = int(stockid)
                query_param['gen_time_begin'] = int(query_param['gen_time_begin'])
                query_param['gen_time_end'] = int(query_param['gen_time_end'])
            except:
                abort(500)
            query_param['stockid'] = stockid
            query_param['tablename'] = 'deal_five'
            return make_resp(scan_db(query_param))
        else:
            result = rclient.hget('deal_five',stockid)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}

class Trade(Resource):
    def get(self, stockid):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not stockid:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            try:
                stockid = int(stockid)
                query_param['gen_time_begin'] = int(query_param['gen_time_begin'])
                query_param['gen_time_end'] = int(query_param['gen_time_end'])
            except:
                abort(500)
            query_param['stockid'] = stockid
            query_param['tablename'] = 'trade_info'
            return make_resp(scan_db(query_param))
        else:
            result = rclient.hget('trade_info',stockid)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}

class Info(Resource):
    def get(self, stockid):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not stockid:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            try:
                stockid = int(stockid)
                query_param['gen_time_begin'] = int(query_param['gen_time_begin'])
                query_param['gen_time_end'] = int(query_param['gen_time_end'])
            except:
                abort(500)
            query_param['stockid'] = stockid
            query_param['tablename'] = 'detail_hyinfo'
            return make_resp(scan_db(query_param))
        else:
            result = rclient.hget('stock_info',stockid)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}

class Tag(Resource):
    def get(self):
            result = rclient.get('tag')
            if result:
                try:
                    return json.loads(result)
                except:
                    print(traceback.print_exc())
                    return {}

class Sumary(Resource):
    def get(self):
            result = rclient.get('sumary')
            if result:
                try:
                    return json.loads(result)
                except:
                    print(traceback.print_exc())
                    return {}

class Kline(Resource):
    def get(self, stockid):
        global parser
        args = parser.parse_args()
        parser.add_argument('gen_time_begin', location=['json', 'args'])
        parser.add_argument('gen_time_end', location=['json', 'args'])
        query_param = dict(args)
        if not stockid:
            abort(404)
        if 'gen_time_begin' in query_param and 'gen_time_end' in query_param and query_param['gen_time_begin'] and query_param['gen_time_end']:
            try:
                stockid = int(stockid)
                query_param['gen_time_begin'] = int(query_param['gen_time_begin'])
                query_param['gen_time_end'] = int(query_param['gen_time_end'])

            except:
                abort(500)
            query_param['stockid'] = stockid
            query_param['tablename'] = 'kline_info'
            return make_resp(scan_db(query_param))
        else:
            result = rclient.hget('kline_info',stockid)
            if result:
                try:
                    data = json.loads(result)
                    return make_resp(data)
                except:
                    print(traceback.print_exc())
                    return {}

api.add_resource(Recommend, '/recommend/<string:tag_name>')
api.add_resource(Sell, '/sell/<string:tag_name>')
api.add_resource(Buy, '/buy/<string:tag_name>')
api.add_resource(SellDetail, '/selldetail/<string:tag_name>')
api.add_resource(BuyDetail, '/buydetail/<string:tag_name>')
api.add_resource(RecommendDetail, '/recommenddetail/<string:tag_name>')
api.add_resource(Five, '/five/<string:stockid>')
api.add_resource(Trade, '/trade/<string:stockid>')
api.add_resource(Info, '/info/<string:stockid>')
api.add_resource(Tag, '/tag')
api.add_resource(Sumary, '/sumary')
api.add_resource(Kline, '/kline/<string:stockid>')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555, debug=True)

