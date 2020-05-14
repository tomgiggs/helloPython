#encoding=utf8

from locust import Locust, TaskSet, task, between,HttpLocust
from locust import HttpLocust, TaskSet, between
import requests
def search(l):
    header = {
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "sdp_app_id": "2353d7e4-cbdc-4962-aadf-16b80a325bf4",
        "language": "zh-CN",
        "Authorization": 'Bearer "F4138BF83405E3B1255DF74A183ECE2909B66759ABC17160FCF517CBCDA1DA0D8FD0C149F912173D39AEB70C34C6368151B6F5760B5A0B7D-00000000"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Origin": "http://studio.edbox-dev.101.com",
        "Referer": "http://studio.edbox-dev.101.com/web/",
    }
    # l.client.post("/login", {"username":"ellen_key", "password":"education"})
    url = "http://api.edbox-dev.101.com/v0.1/api/product/product/actions/search_app?word=&page=1&size=30&popular&searchPlatforms=WINDOWS,WEB_PC&usesId=10000286"
    with l.client.get(url,  catch_response=True, headers=header, verify=False) as response:
        # assert response.json()['rating']['max']==10            #python断言对接口返回值中的max字段进行断言
        if response.status_code == 200:  # 对http响应码是否200进行判断
            response.success()
        else:
            print(response.text)
            # ll = requests.get()
            # ll.text
            response.failure("GetActConfig[Failed!]")
def logout(l):
    l.client.post("/logout", {"username":"ellen_key", "password":"education"})

def index(l):
    l.client.get("http://api.edbox-dev.101.com/")

def profile(l):
    l.client.get("http://api.edbox-dev.101.com/profile")

class UserBehavior(TaskSet):
    # tasks = {index: 2, profile: 1}
    @task(1)# 没有这个的话就会报：IndexError: Cannot choose from an empty sequence
    def on_start(self):
        search(self)

    def on_stop(self):
        # logout(self)
        pass

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1.0, 9.0) # 注释掉会报错： You must define a wait_time method on either the WebsiteUser or UserBehavior class
    # min_wait = 3000  # 单位为毫秒
    # max_wait = 6000  # 单位为毫秒