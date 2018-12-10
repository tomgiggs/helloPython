import traceback

# from zkclient import ZKClient, zookeeper, watchmethod
# '''
# linux安装zookeeper
# 然后编译安装c客户端，ln -s /data/zookeeper/zookeeper-3.4.13/src/libs/*.so* /usr/lib把生成的动态链接库复制到一个新的路径然后链接到/usr/lib下面
# 之后通过ldconfig使链接生效，最后安装zkpython，或者其他Python模块来使用zookeeper
# '''
# from os.path import basename, join
# zkhost='127.0.0.1:2181'
# zkpath = '/'
# es_path = join(zkpath,'es')
# master_num = 1
# timeout = 5000
# zkclient = ZKClient(zkhost,timeout)
# node = (zkpath,es_path)
# if zkclient.exists(node):
#     print('es path exist')
# else:
#     try:
#         zkclient.create(node,'')
#     except:
#         print(traceback.print_exc())



import logging
from time import sleep
from kazoo.client import KazooClient
from kazoo.client import KazooState
#zk = KazooClient('127.0.0.1:2181')
zk = KazooClient('127.0.0.1:2181',auth_data=[('digest', 'user01:123456')])
zk.start()
#zk.add_auth("digest",'user01:123456')
#zk.start()
zk.ensure_path("/1/2/3")
def my_listener():
    print(zk.state)
    if zk.state == "LOST":
        print("zk lost")# Register somewhere that the session was lost
    elif zk.state == "SUSPENDED":
        print("wait for reconnecting")
    else:
        print("zk fine")


def children_callback(children):
    print('****',children)

children = zk.get_children('/zookeeper', children_callback)
my_listener()
zk.create('/goodboy1236456',ephemeral=True,value=b'xxxxxxxxxxxxxxxxxxxx')
#zk.delete('/zookeeper/555555')
xx = zk.ChildrenWatch("/zookeeper/goodboy12364567777")
print(xx.__dict__)

def outprint(event):
    print(event)
y=zk.get('/rookie0000000000',watch=outprint)
#zk.add_listener(outprint)

@zk.ChildrenWatch("/")
def watchdemo(children):
    print(children)
import time
time.sleep(60) #只要不退出，zookeeper就会中的节点就会一直存在，
# 通过这样的方式来一直保持节点存活，kazoo本身是没有那种可以后台运行的方法的，是通过程序不退出来维持的






