
# import etcd3
# #往etcd中存数据
# client = etcd3.client(host='192.168.133.140')   #连接etcd
# r  = client.put('aaa', 'qweqwe')              #往etcd中存键值
# b = client.get('aaa')                        #查看etcd中的键值
# vents_iterator, cancel = client.watch('aaa')         #监听etcd中aaa键 是否发生改变，
# print(vents_iterator).value

import consul
# http://172.24.140.36:8500/ui/dc1/services
c = consul.Consul('172.24.140.36')
# c.connect('172.24.140.36',8300,'good')
# poll a key for updates
index = None
while True:
    index, data = c.kv.get('foo', index=index)
    print(data['Value'])
    break

# in another process
# c.kv.put('foo', 'bar')