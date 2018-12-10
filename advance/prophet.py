# import  prophet as ph
# import pandas as pd
# import numpy as np
#
# #source = open(r'd:\data\germany_sales_2017.csv','r')
# sin = pd.read_csv('d:\data\germany_sales_2017.csv',header=0,sep='\t').fillna(0)
# print(sin)
from twisted.internet import reactor,defer,protocol,task
import time

def out(s):
    print(s)


def add_callback():
    num = 1
    while True:
        d = defer.Deferred()
        call_info = 'this is info :' + str(num)
        num += 1
        #reactor.callWhenRunning(d.callback, 'Another short poem.')
        d.addCallbacks(out,out)
        d.callback(call_info)
        time.sleep(2)


add_callback()
