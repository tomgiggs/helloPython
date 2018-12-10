#encoding=utf8
import pymysql
# import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker

connect = create_engine("mysql+pymysql://root:root@localhost:3306/investment",
                        encoding="utf-8",
                        echo=True)  # 连接数据库，echo=True =>把所有的信息都打印出来

Base = declarative_base()  # 生成ORM基类
#
#
class User(Base):
    __tablename__ = "hello_word"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))


# Base.metadata.create_all(connect)  # 创建表结构

session_class = sessionmaker(bind=connect)  # 创建与数据库的会话session class ,这里返回给session的是个class,不是实例
session = session_class()   # 生成session实例
# obj = User(name="test", password="1234")  # 生成你要创建的数据对象
# session.add(obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
# session.commit()  # 统一提交，创建数据，在此之前数据库是不会有新增数据的

# 新增多条数据

# users = []
# for i in range(20):
#     obj = User(name="test"+str(i), password="1234"+str(i))
#     users.append(obj)
# session.add_all(users)
# session.commit()
#删除数据
# session.query(User).filter(User.id > 5).delete()
# session.commit()
result = session.query(User.name,User.id).filter_by(name='test1').all()
for r in result:
    print(r.__dict__)



