import pymongo
client=pymongo.MongoClient("localhost",27017)
db=client.zhihu
datas=db.user.find()
for x in datas:
    if x.get("url")!=None:
        print x.get("url")