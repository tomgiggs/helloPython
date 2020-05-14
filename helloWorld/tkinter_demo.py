import _tkinter
# encoding=utf8

# import Tkinter

from tkinter import *# python3.2之前使用这个来导入：from TKinter import *
from kafka import KafkaConsumer, TopicPartition

root = Tk()
root.title("kafka查询")
root.geometry('300x300')

def start(*args, **kwargs):
    topic_name = topic.get()
    server_host = server.get()
    server_host = server_host + ':9092'
    print(server_host)
    t_partition = partition.get()
    if not t_partition:
        t_partition = 0
    group = group_id.get()
    #print topic_name,server_host,t_partition,group
    # 指定分区的指定offset开始消费
    consumerx = KafkaConsumer(topic_name, bootstrap_servers=[server_host, ], auto_offset_reset='earliest', group_id=group, )
    consumerx.unsubscribe()
    consumerx.assign([TopicPartition(topic=topic_name, partition=0), ])  # 指定分区订阅
    record_num = consumerx.end_offsets([TopicPartition(topic=topic_name, partition=t_partition), ])
    t.insert(1.0, record_num)


Label(root, text="话题").grid(row=0, sticky=W)
topic = StringVar()
Entry(root, textvariable=topic).grid(row=0, column=1, sticky=W)
# topic_name.pack() #不能加pack加了就显示不出来了
Label(root, text="服务器ip").grid(row=1)
server = StringVar()
Entry(root, textvariable=server).grid(row=1, column=1)
Label(root, text="消费者组").grid(row=2)
group_id = StringVar()
Entry(root, textvariable=group_id).grid(row=2, column=1)
Label(root, text="分片").grid(row=3)
partition = StringVar()
Entry(root, textvariable=partition).grid(row=3, column=1)
Button(root, text="查询", bg="green", command=start).grid(row=5, column=2)
# frame = Frame(root,height=20,width = 100)
t = Text(root, height=20, width=100,setgrid=True)
t.grid(row=4, column=1)

root.mainloop()
