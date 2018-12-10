#encoding=utf8
# def func(x,y,z):
#     print('this is a lambda test')
#     print(x+y+z)
#
# dunc = lambda x,y,z: func(x,y,z)
#
# dunc(1,2,3)
from twisted.internet import reactor,defer,protocol,task
from twisted.internet.defer import inlineCallbacks
import time

i = 0

def defer_generator():
    d = defer.Deferred()
    d.addCallbacks(on_success,on_failed)
    d.addBoth(call_back2)
    d.addBoth(call_back3)
    # reactor.callWhenRunning(d.callback, 'hello world,this is a begin')
    return d


    pass



def begin_loop():
    d = None
    d = defer_generator()
    reactor.callWhenRunning(d.callback, 'hello world,this is a begin')
    reactor.run()
    num = 1
    # while True:
    #     call_info = 'this is info :' + str(num)
    #     num += 1
    #     d.callback(call_info)


    pass

def call_back2(info):
    print('this call back 2')
    pass

def call_back3(info):
    print('this call back 3')
    pass

@inlineCallbacks
def on_success(info):
    #print 'callback success'
    global i
    print info
    d = defer_generator()
    # while True:
    # d = defer.Deferred()
    # d.addBoth(call_back2)
    return d
    #reactor.run()

    # d.addCallbacks(on_success, on_failed)
    # call_info = 'this is info :' + str(i)
    # i += 1
    # time.sleep(1)
    #reactor.callWhenRunning(d.callback, 'back2')
    # reactor.run()
    #reactor.stop()


    pass


def on_failed(info):
    print('callback failed')
    #reactor.stop()


    pass

def add_callback():

    pass




begin_loop()

