import thread
import threading
import time
def spider():
    time.sleep(1)
    print 'hello x'
    for x in range(20, 50):
        print x
class testSpider(threading.Thread):
    def __init__(self):
        super(testSpider,self).__init__()
    def run(self):
        time.sleep(3)
        print 'i am '+self.getName()
        for x in range(20,50):
            print x


'''
t=testSpider()
print 'this is main thread'
#run() is different from start()
t.run()
#t.start()
print 'i will game over'
'''
'''
t=threading.Thread(target=spider)
t.start()
t.join()
print 'main thread..'
'''