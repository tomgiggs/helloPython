#-*- coding: UTF-8 -*-
import json
import pickle
class jsonTest(object):
    def __init__(self):
        self.name=''
        self.age=24

    def hello(self):
        print 'i am yiong'
'''
yilong=jsonTest()

yilong.hello()
'''
'''
d=json.dump(yilong)
print d
'''
'''
weather=open('d:\weather.json','r+').read()
convert=weather.decode('GB2312').encode('utf-8')
#print convert
iamjson=json.dumps(convert)
test=json.loads(convert)
#print type(iamjson)
print type(test)
print test
#print iamjson
'''


#change string's coding
def convert():
    file = open('d:\weather.json', 'a+')
    weather = file.read()

    converted = weather.decode('GB2312').encode('utf-8')
    file.write(converted)
    file.close()

convert()
f=open('d:\weather.json','r+').read()
print f


