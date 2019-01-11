# encoding=utf8
import time


def exc_time(func):
    def deco(a, b):
        begin_time = time.time()
        time.sleep(1)
        func(a, b)
        end_time = time.time()
        print end_time - begin_time

    return deco


@exc_time  # 加了装饰器后就是把函数调用关系转移到装饰器上（把调用的函数名及参数传递给装饰器
def service_func(a, b):
    print a + b


service_func(1, 5)
