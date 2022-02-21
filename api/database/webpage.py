import os
from sqlite3 import Cursor
import pymysql
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASS = os.environ.get("MYSQL_PASS", "123456")
MYSQL_DB = os.environ.get("MYSQL_DB", "softlion")
# print(MYSQL_HOST)
# print(MYSQL_USER)
# print(MYSQL_PASS)
# print(MYSQL_DB)
connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)

def select_WebPage(Url):
    # print('查找一条网站数据')
    # 进行查找
    # print(Url)
    cursor = connection.cursor
    result = cursor.execute("select * from WebPage where Url = '{}';".format(Url))
    # print(Url)
    # print(result)
    if result > 0:
        # print('查找成功')
        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result
    else:
        cursor.close()
        # print('查找失败')
        return -1

# 插入网站
def insert_WebPage(Url):
    # print(WebPage)
    # print(WebPage.Url)
    cursor = connection.cursor()
    # 如果已经存在则删除
    tmp = select_WebPage(Url)
    if tmp != -1 and len(tmp) > 0:
        return 

    # print('插入一条网站数据')
    # 进行插入
    result = cursor.execute("INSERT INTO WebPage VALUES( '{}', {}, {} );".format(Url, StateMent, Count))
    # 提交执行
    connection.commit()
    # if result > 1:print('插入成功')
    # else:print('插入失败')