import MySQLdb
def query():
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='zhihu_info', port=3306)
        cur = conn.cursor()
        cur.execute('select * from user')
        for x in cur.fetchall():
            print x

        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def insert():
    #try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='zhihu_info', port=3306)
        cur = conn.cursor()
        name='yilongXxxx'
        care='100'
        agree='30'
        thank='50'
        collection='32'
        sql="insert into user(name,care_num,agree_num,thank_num,collection_num)values('%s',%s,%s,%s,%s)"%(name,care,agree,thank,collection)
        cur.execute(sql)
        conn.commit()
        cur.close()

        conn.close()
        print 'ok'

    #except MySQLdb.Error,e:
       # print 'error'


'''
name='yilong'
care='100'
agree='30'
thank = '50'
collection = '32'
sql = 'insert into user values (%d,"%s",%s,%s,%s,%s)'%(12,name, care, agree, thank, collection)
#print sql
'''
insert()
#query()