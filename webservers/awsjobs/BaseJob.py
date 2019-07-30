# encoding=utf8
import threading
# import thread
import time


class Jobs(object):
    lock = threading.Lock()

    def __init__(self):
        self.jobs_Num = None
        self.server_list = []
        self.country_list = ['au', 'ca', 'de', 'es', 'fr', 'it', 'in', 'jp', 'mx', 'gb', 'us']
        self.job_list = [{'tableName': '011', 'url': '', 'country': 'au'},
                         {'tableName': '012', 'url': 'www.us.com', 'country': 'us'},
                         {'tableName': '013', 'url': '', 'country': 'de'},
                         {'tableName': '014', 'url': '', 'country': 'fr'}]
        self.running_job_list = []
        self.finshed_job_list = []
        self.failed_list = []

    def __new__(cls, *args, **kwargs):
        if not hasattr(Jobs, "_instance"):
            with Jobs.lock:
                if not hasattr(Jobs, "_instance"):
                    Jobs._instance = object.__new__(cls)
        return Jobs._instance



        pass


    def register(self, ip):
        country = None
        if self.lock.acquire():
            time.sleep(2)
            country = self.country_list.pop()
            self.lock.release()
            return country

        self.server_list.append({'serverip': ip, 'country': ''})
        return country

    def set_job(self, job):
        job = {'tableName': '', 'url': '', 'country': ''}
        if self.lock.acquire():
            time.sleep(2)
            self.job_list.append(job)
            self.lock.release()
            return job

    def finsh_report(self, report):

        # report = {'serverip': '', 'finsh_time': '', 'begin_time': '', 'tableName': '', 'record_num': ''}
        job = report['tableName']
        for j in self.running_job_list:
            if j['tableName'] == job:
                self.running_job_list.remove(j)
        self.running_job_list.remove(job)
        self.finshed_job_list.append(report)
        return

    def get_job(self, country, serverip):
        job = None
        if self.lock.acquire():
            time.sleep(2)
            for item in self.job_list:
                if item['country'] == country:
                    job = item
                    self.running_job_list.append({'tableName': job['tableName'], 'serverip': serverip})
                    self.job_list.remove(item)
                    break
            self.lock.release()
            return job
