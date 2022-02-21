import os
from unittest import result
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

# 建立表单（WebPage）表单
# Url 为网址
# Statement 是否可以访问
# Count 访问失败次数
connection.cursor().execute("CREATE TABLE IF NOT EXISTS `WebPage`(\
    `Url` VARCHAR(1024) NOT NULL,\
    `StateMent` INT,\
    `Count` INT,\
   PRIMARY KEY ( `Url` )\
)ENGINE=InnoDB DEFAULT CHARSET=utf8;")
# connection.cursor().execute("delete from WebPage;")
# 查找网站
def select_WebPage(cursor, Url):
    # print('查找一条网站数据')
    # 进行查找
    # print(Url)
    result = cursor.execute("select * from WebPage where Url = '{}';".format(Url))
    # print(Url)
    # print(result)
    if result > 0:
        # print('查找成功')
        result = cursor.fetchall()
        return result
    else:
        # print('查找失败')
        return -1

def select_all_WebPage_Url(cursor):
    # 选取所有的Url
    result  = cursor.execute("select Url from WebPage;")
    # 返回受影响的行数
    return result

def select_all_webPage_Url(cursor):
    # 初始化游标
    tmpcursor = connection.cursor(pymysql.cursors.DictCursor)
    # 进行查询
    tmpcursor.execute("select Url from WebPage;")
    # 得到返回值
    lst = tmpcursor.fetchall()
    # 关闭游标
    tmpcursor.close()
    # 返回结果
    return lst

# 删除网站
def delete_WebPage(cursor, Url):
    # print('删除一条网站数据')
    # 进行删除
    result = cursor.execute("DELETE FROM WebPage WHERE Url = '{}';".format(Url))
    # 提交执行
    connection.commit()
    # if result > 1:print('删除成功')
    # else:print('删除失败')

# 插入网站
def insert_WebPage(cursor, WebPage):
    # print(WebPage)
    # print(WebPage.Url)
    Url = str(WebPage.Url)
    StateMent = int(WebPage.StateMent)
    Count = int(WebPage.Count)

    # 如果已经存在则删除
    tmp = select_WebPage(cursor, Url)
    if tmp != -1 and len(tmp) > 0:
        delete_WebPage(cursor, Url)

    # print('插入一条网站数据')
    # 进行插入
    result = cursor.execute("INSERT INTO WebPage VALUES( '{}', {}, {} );".format(Url, StateMent, Count))
    # 提交执行
    connection.commit()
    # if result > 1:print('插入成功')
    # else:print('插入失败')


# 更新网站
def update_WebPage(cursor, WebPage):
    pass

if __name__=='__main__':
    connection.cursor().execute("drop table Log;")
    connection.cursor().execute("CREATE TABLE IF NOT EXISTS `Log`(\
        `date` DATETIME NOT NULL,\
        `2` INT,\
        `4` INT,\
        `5` INT,\
        `9` INT,\
    PRIMARY KEY ( `date` )\
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;")
    connection.close()