def deco(func):
    def wrapper():
        print 'i am decorator'
        func()
    return wrapper()
@deco
def helloDeco():
    print 'i was be decorated'

helloDeco()