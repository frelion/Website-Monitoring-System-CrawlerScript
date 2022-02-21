import os
import pymysql
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASS = os.environ.get("MYSQL_PASS", "123456")
MYSQL_DB = os.environ.get("MYSQL_DB", "softlion")
def select_all_WebPage_Url(cursor):
    # 选取所有的Url
    result  = cursor.execute("select Url from WebPage;")
    # 返回受影响的行数
    return result
def db_url():
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    )
    # 临时游标
    tmpcursor = connection.cursor()
    # 访问数据库并且返回数据总量
    select_all_WebPage_Url(tmpcursor)
    # 进行迭代器遍历
    i = 0
    for url in tmpcursor:
        i += 1
        yield i,url['Url']
    # 关闭临时游标
    tmpcursor.close()
    connection.close()
    return -1,-1

def select_all_statement():
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    )
    # 临时游标
    cursor = connection.cursor()
    cursor.execute("select StateMent from WebPage;")
    connection.commit()
    for sm in cursor:
        yield sm['StateMent']
    cursor.close()
    connection.close()
    return -1
    
def update(url, statement):
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    )
    # 临时游标
    cursor = connection.cursor()
    cursor.execute("update WebPage set StateMent = {} where url = '{}';".format(statement, url))
    connection.commit()
    cursor.close()
    connection.close()

def selectcount():
    se = dict()
    for sm in select_all_statement():
        if sm==-1:continue
        sm = sm // 100
        se[sm] = se.get(sm,0)+1
    return se

def execute(sql):
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    )
    # 临时游标
    cursor = connection.cursor()
    lst = []
    try:
        cursor.execute(sql)
        connection.commit()
        lst = [item for item in cursor]
    finally:
        cursor.close()
        connection.close()
    return lst

if __name__=='__main__':
    sql = "select * from Log ORDER BY date DESC limit 0,10;"
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    )
    # 临时游标
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        for item in cursor:
            print(item)
    finally:
        cursor.close()
        connection.close()