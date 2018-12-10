#encoding=utf8
import psycopg2

client = psycopg2.connect(database="investment", user="postgres", password="cyl123", host="127.0.0.1", port="5432")
cursor = client.cursor()
cursor.execute("SELECT PROJ_ID,INDUSTRY_ID,PROJ_NAME,PROJ_APP,TOTAL_INVESTMENT,APPLICATE_AREA,BUILD_AREA,BUILD_ADDRESS,LINKMAN  FROM test004 limit 10")
result = cursor.fetchall()
for r in result:
    print(r)





