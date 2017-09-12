import redis
good=redis.Redis(host="127.0.0.1",port=6379,db=0)
#good.sadd("urls","https://www.zhihu.com/people/")
#for x in good.smembers("urls"):
#    print x
print good.spop("urls")