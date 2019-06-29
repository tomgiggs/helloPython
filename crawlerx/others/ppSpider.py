#encoding=utf8
#澎湃新闻爬虫
import json
import os
import time
import traceback
from lxml import etree
import requests
import random
from multiprocessing import process
from threading import Thread
user_agents = json.loads(open('crawlerx/useragents.json').read())

#美团技术文章链接：https://tech.meituan.com//page/66.html，有空再爬
header = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    # "Connection":"close",
    "User-Agent":"",
    "Cache-Control": "no-cache",
    "Cookie":"UM_distinctid=16b9377b0bf4de-0cc07dd30e03bf-e343166-232800-16b9377b0c09cd; aliyungf_tc=AQAAAJSX8itICAgAneRabuzg5mxwbuRU; __ads_session=KcTmbLjQTgmdsaMDFAA=; Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1561547223,1561601848; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1561601848; CNZZDATA1261102524=509074382-1561546649-null%7C1561598061; route=030e64943c5930d7318fe4a07bfd2a3c; JSESSIONID=22E83CBB7866CFC18116C3206F66CA68; uuid=d134a4f8-7150-40f1-b5a0-7e2e46cb622f; SERVERID=srv-omp-ali-portal12_80",
    # "Host":"www.thepaper.cn",
    "Upgrade-Insecure-Requests":"1"
}

def clean_data(body):
    if body:
        xxx = " ".join(body).replace("\n", "").replace("\t", "").replace(" ", "")
    else:
        xxx = ""
    return xxx

# begin_index = 1291995
#    for i in range(3760556,3770655):
def start(start_index,end_index):
    httpClient = requests.session()
    news_count = 0
    file_out = open('pengpai_news_'+str(start_index), 'a+', encoding='utf8')
    agent = ""
    for i in range(start_index,end_index):
        agent = random.choice(user_agents['browsers']['chrome'])
        # header['User-Agent']= agent,#???为什么打印出来的user-agent会变成带有括号的元组呢？？特么agent后面多了一个逗号。。。。。
        header['User-Agent'] = agent
        try:
            url = 'https://www.thepaper.cn/newsDetail_forward_'+str(i)
            result = httpClient.get(url, headers=header)
            html = etree.HTML(result.text)
            if html:
                news_data = html.xpath('//div[@class="news_txt"]//text()')
                news_title = html.xpath('//h1[@class="news_title"]//text()')
                news_about = html.xpath('//div[@class="news_about"]//p//text()')
            else:
                continue
            news_about = clean_data(news_about)
            news_title = clean_data(news_title)
            news_data = clean_data(news_data)
            news_line = str(i)+"|++|"+news_title+"|++|"+news_about+"|++|"+news_data+"\n"
            if news_data:
                file_out.write(news_line)
                file_out.flush()
                news_count +=1
            if news_count==1000:
                file_out.close()
                file_out = open('pengpai_news_'+str(i), 'a+', encoding='utf8')
                news_count = 0
        except Exception as e:
            traceback.print_exc()
            # print(e.with_traceback())
            time.sleep(10)
            pass
        time.sleep(0.01)
    file_out.close()


def multiProcess():
    begin=2694450
    for i in range(8):
        t = Thread(target=start, name=i, args=(begin,begin+100000))
        t.start()
        begin += 100000

multiProcess()
