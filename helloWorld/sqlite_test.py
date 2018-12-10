#encoding=utf8
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('user.db')
conn.row_factory = dict_factory
#conn.execute("CREATE TABLE user_info(ID INT PRIMARY KEY  NOT NULL, NAME TEXT  NOT NULL, PASSWD  INT   NOT NULL, ADDRESS CHAR(50) );")
cursor = conn.cursor()
#cursor.execute("insert into user_info values (2,'test02','123456','fujian,zhanghzou')",)
#conn.commit()
table = cursor.execute('select * from user_info')
ta = table.fetchall()

for x in ta:
    print(x)


#encoding=utf8
# import sqlite3
# connection = sqlite3.connect('./instance/user.db')
# cursor = connection.cursor()
# cursor.execute('select * from user')
# results = cursor.fetchall()
# for r in results:
#     print(r)
# print(results)


