from twisted.internet import reactor,defer
import time


def get_info(info):
    print(info)
    d.addCallbacks(get_info, get_info_error)
    pass

def send_info():
    while True:
        time.sleep(2)
        return "this is a test info"

    pass
def get_info_error(error):
    print(error)
    pass
def send_info_error(error):
    print(error)
    pass
def stop_server():
    reactor.stop()
    pass


def start_server():
    d = defer.Deferred()
    d.addCallbacks(get_info, get_info_error)
    reactor.callWhenRunning(d.callback, send_info())
    reactor.run()

start_server()

#
# def test_2(y):
#     #raise Exception
#     return y*6
#
# def test_yield():
#     print('begin func')
#     x = 100
#     i = 4
#     x = yield 4*80
#     print x
#     # for i in range(5):
#     #     x = yield test_2(i)
#     #     print x
# ok = test_yield()
# print ok.next()
# print(ok.next())
# # print(ok.next())
# # print(ok.next())
# # print(ok.next())
