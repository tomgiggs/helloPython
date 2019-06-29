# encoding=utf8
# 网易用户歌单列表爬虫，可以看到用户的隐藏歌单。。。
#参考 https://github.com/darknessomi/musicbox/blob/master/NEMbox/api.py
import json
import os
import time
import traceback
import requests
import random
from threading import Thread
import pymongo
mongo_config = {
    'host': '127.0.0.1',
    'port': 27017,
    'db': 'netease_music',

}
try:
    conn = pymongo.MongoClient(mongo_config['host'], mongo_config['port'])
    db = conn[mongo_config['db']]

except Exception:
    print(traceback.format_exc())


user_agents = json.loads(open('../crawlerx/useragents.json').read())

header = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "",
    "Cache-Control": "no-cache",
    "Cookie": "UM_distinctid=16b9377b0bf4de-0cc07dd30e03bf-e343166-232800-16b9377b0c09cd; aliyungf_tc=AQAAAJSX8itICAgAneRabuzg5mxwbuRU; __ads_session=KcTmbLjQTgmdsaMDFAA=; Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1561547223,1561601848; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1561601848; CNZZDATA1261102524=509074382-1561546649-null%7C1561598061; route=030e64943c5930d7318fe4a07bfd2a3c; JSESSIONID=22E83CBB7866CFC18116C3206F66CA68; uuid=d134a4f8-7150-40f1-b5a0-7e2e46cb622f; SERVERID=srv-omp-ali-portal12_80",
    "Upgrade-Insecure-Requests": "1"
}
playlist_collection = db.get_collection('playlist')
user_info_collection = db.get_collection('user_info')
song_info_collection = db.get_collection('song_info')
def process_msg(data):
    try:
        body = json.loads(data)
        if 'result' in body:
            body = body['result']
        else:
            return False

        user_info = body.pop('creator')
        user_info['_id'] = user_info['userId']
        song_list = body.pop('tracks')
        song_id = []
        for song in song_list:
            song_id.append(song['id'])
            song['_id'] = song['id']
            song_info_collection.insert_one(song)
        body['creator'] = user_info['userId']
        body['musicList'] = song_id
        body['_id'] = body['id']
        playlist_collection.insert_one(body)
        user_info_collection.insert_one(user_info)
    except pymongo.errors.DuplicateKeyError as e01:
        return True
        pass
    except  Exception as e:
        traceback.print_exc()
        return True
        pass


def start(start_index, end_index):
    httpClient = requests.session()
    news_count = 0
    file_out = open('netease_musics_' + str(start_index), 'a+', encoding='utf8')
    for i in range(start_index, end_index):
        agent = random.choice(user_agents['browsers']['chrome'])
        header['User-Agent'] = agent
        try:
            url = 'http://music.163.com/api/playlist/detail?id=' + str(i)
            result = httpClient.get(url, headers=header)
            jsonData = result.text
            if not jsonData:
                continue
            if jsonData:
                retult = process_msg(jsonData)
                if result:
                    file_out.write(jsonData+"\n")
                    file_out.flush()
                    news_count += 1
            if news_count == 300:
                file_out.close()
                file_out = open('netease_musics_' + str(i), 'a+', encoding='utf8')
                news_count = 0
        except Exception as e:
            traceback.print_exc()
            time.sleep(10)
        time.sleep(0.01)
    file_out.close()


def multiProcess():
    begin = 150000
    for i in range(6):
        t = Thread(target=start, name=i, args=(begin, begin + 10000))
        t.start()
        begin += 10000

multiProcess()
