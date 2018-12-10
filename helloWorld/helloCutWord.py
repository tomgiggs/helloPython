#encoding=utf8

import jieba
from collections import Counter
import time
import threading
import chardet
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


file=open(r'd:\redbuilding.txt')
text=file.read()
file.close()
strs=r'早在2个月之前，大聪已经写了一份《猩球崛起》系列终极指南报告，早在还没来得及看《猩球崛起3》的小伙伴（无严重剧透），可放心食用，时空门'
result=jieba.cut(text,cut_all=True)
convert=[]
for x in result:
    convert.append(x)
result=convert
print(len(result))

'''
#sentence=','.join(result) #这个会清空result
#print sentence
print result
print type(result)

'''
'''
result = dict(Counter(result))
with open(r'd:\result.txt', 'w') as fw:
    for k, v in result.items():
        fw.write("%s,%d\n" % (k, v))
'''
begintime=time.time()
#print sentence
def tongji():

    huizong = {}
    result2 = result
    for a in result:
        #print a
        count = 1
        result2.remove(a)
        for x in result2:
            if x==a:
                count+=1
                result2.remove(x)


        huizong[a]=count

    #sorted(huizong.items(), key=lambda x: x[1], reverse=True)
    for k,v in huizong.items():
        print(k,v)


    with open(r'd:\result.txt', 'w') as fw:
        for k, v in huizong.items():
            output=str(k)+str(v)+'\n'
            fw.write(output)#???UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
            #fw.write("%s,%s \n"%(k,v))
            #fw.write("{key}{value} \n".format(key=k, value=v))
