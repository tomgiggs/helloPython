#encoding=utf8

from thrift.transport import TSocket,TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import ColumnDescriptor
from hbase.ttypes import Mutation,BatchMutation
from hbase.ttypes import Mutation

# thrift默认端口是9090
socket = TSocket.TSocket('192.168.99.100',9090)
socket.setTimeout(8000)
transport = TTransport.TBufferedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Hbase.Client(protocol)
socket.open()

tables = client.getTableNames()
print(tables) #['db01:table01', 'demo2', 'project_info']
client.getTableRegions('db01:table01')


# print(client.getTableNames())
column_data = client.get('db01:table01','row01','address:province')#获取具体行具体列的信息
print(type(column_data))
print(column_data[0].value)
print(column_data) #[TCell(timestamp=1543680680608L, value='yunnan')]

row_data = client.getRow('db01:table01','row01') #获取一行的全部信息
#获取多条数据
scanid = client.scannerOpen('tablepy','row01',['addr_info'])#如果列不存在会怎么样？NoSuchColumnFamilyException: Column family addre_info does not exist in region tablepy
# while(True):
#     result = client.scannerGet(scanid)
#     print(result)
#     if not result:
#         break


rows_data = client.scannerGetList(scanid,20)
for data in rows_data:
    print(data)
client.scannerClose(scanid)

print(row_data) #[TRowResult(columns={'address:province': TCell(timestamp=1543680680608L, value='yunnan')}, row='row01')]
column01 = ColumnDescriptor(name='user_info') # ColumnDescriptor(bloomFilterType='NONE', bloomFilterNbHashes=0, name='user_info', maxVersions=3, blockCacheEnabled=False, inMemory=False, timeToLive=-1, bloomFilterVectorSize=0, compression='NONE')
column02 = ColumnDescriptor('addr_info')
#hbase好像不支持使用Python创建预分区表
# client.createTable('tablepy',[column01,column02])
# print(client)
region_info = client.getTableRegions('tablepy')#查看表分区
table_info = client.getColumnDescriptors('tablepy')#查看表结构
print(region_info) # [TRegionInfo(startKey='', endKey='', version=1, id=1543752131747L, name='tablepy,,1543752131747.ccfa71e67b9732adb575129bf9e560eb.')]
print(table_info) # {'addr_info:': ColumnDescriptor(bloomFilterType='NONE', bloomFilterNbHashes=0, name='addr_info:', maxVersions=3, blockCacheEnabled=False, inMemory=False, timeToLive=2147483647, bloomFilterVectorSize=0, compression='NONE'), 'user_info:': ColumnDescriptor(bloomFilterType='NONE', bloomFilterNbHashes=0, name='user_info:', maxVersions=3, blockCacheEnabled=False, inMemory=False, timeToLive=2147483647, bloomFilterVectorSize=0, compression='NONE')}
#插入数据
mutation = Mutation(column='user_info:province',value='350000')
batchs = BatchMutation('row02',[mutation])
insert_resut = client.getRow('tablepy','row01')
#插入多条数据
# client.mutateRow('tablepy','row01',[mutation])
client.mutateRows('tablepy',[batchs]) #这个方法与上面mutateRow的区别在于，mutateRows可以一次插入多条记录，而mutateRow只能插入单条数据
print(insert_resut) # [TRowResult(columns={'user_info:province': TCell(timestamp=1543752270954L, value='350000')}, row='row01')]
client.deleteAll('tablepy','row01','addr_info') #删除指定指定行指定列的数据
client.deleteAllRow('tablepy','row01') #删除指定行的全部数据


socket.close() #用完要记得关闭