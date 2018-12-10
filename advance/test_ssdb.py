#encoding=utf8
import time
import redis
from ssdb import SSDB



rclient = redis.Redis(host="*", port=36379, password='**')
rpipeline = rclient.pipeline()

pipe_time = time.time()
for x in range(10000):
    rpipeline.lpop('task_list_test01')
#rpipeline.lrange('task_list_test01',0,10000)
records = rpipeline.execute()
print('redis total time:',time.time()-pipe_time )

sclient = SSDB('*',port=46379)
# sclient = SSDB(host='18.196.*.*',port=46379,)
sclient.execute_command('auth xxxxxxx')
i = 1
begin_time = time.time()
sclient.qpush_front('task_list_sorted',records)
print(time.time() - begin_time)

exit(0)
for record in records:
    # sclient.zset('task_list_sorted',record,i)
    sclient.qpush_front('task_list_sorted',record)
    i += 1
print(time.time() - begin_time)