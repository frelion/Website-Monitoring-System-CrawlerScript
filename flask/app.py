from datetime import datetime
from logging import exception
import requests
from flask import send_from_directory
from flash import database as db
from flask import Flask
from flask_cors import CORS
from flask import request
app = Flask(__name__)
CORS(app)

import os
import pymysql
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASS = os.environ.get("MYSQL_PASS", "123456")
MYSQL_DB = os.environ.get("MYSQL_DB", "softlion")
# print(MYSQL_HOST)
# print(MYSQL_USER)
# print(MYSQL_PASS)
# print(MYSQL_DB)

def select_WebPage(Url):
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    )
    print('查找一条网站数据')
    # 进行查找
    # print(Url)
    cursor = connection.cursor()
    result = cursor.execute("select * from WebPage where Url = '{}';".format(Url))
    # print(Url)
    # print(result)
    if result > 0:
        # print('查找成功')
        result = cursor.fetchall()
        cursor.close()
        # print(result)
        connection.close()
        return result
    else:
        cursor.close()
        connection.close()
        # print('查找失败')
        return -1

def excute(sql):
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    )
    cursor = connection.cursor()
    result = cursor.execute(sql)
    if result > 0:
        # print('查找成功')
        result = cursor.fetchall()
        cursor.close()
        # print(result)
        connection.close()
        return result
    else:
        cursor.close()
        connection.close()
        # print('查找失败')
        return -1

@app.route("/api/helloworld")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/selectWebpageByUrl")
def selectWebpageByUrl():
    res = select_WebPage("https://www.suda.edu.cn/")
    print(res)
    return str(res)

@app.route("/api/select6Webpage")
def select6Webpage():
    res = excute("select * from WebPage limit 0,6;")
    return str(res)
@app.route("/api/searchUrl", methods=["POST"])
def searchUrl():
    data = request.get_json()
    res = select_WebPage(data['url'])
    return str(res[0])
@app.route("/api/deleteUrl", methods = ["POST"])
def deleteUrl():
    data = request.get_json()
    res = -1
    for i in range(3):
        if select_WebPage(data['url']) != -1:
            res = excute("DELETE FROM WebPage WHERE Url = '{}';".format(data['url']))
        else:return None
        if res!=1:return "200"
    return None

@app.route("/api/insertUrl", methods = ["POST"])
def insertUrl():
    data = request.get_json()
    vis = False
    for i in range(3):
        sc = requests.get(data['url'],verify=False).status_code
        if sc == 200:
            vis = True
            break
    if vis:
        res = -1
        for i in range(3):
            if select_WebPage(data['url']) != -1:
                excute("DELETE FROM WebPage WHERE Url = '{}';".format(data['url']))
            res = excute("INSERT INTO WebPage VALUES('{}', 1, 0);".format(data['url']))
            if res!=-1:break
        if res==-1:
            return None
        res = select_WebPage(data['url'])
        print(res)
        return str(res[0])
    return None

@app.route("/api/selectlog")
def selectLog():
    res = db.execute("select * from Log ORDER BY date DESC limit 0,10;")
    for i in range(len(res)):
        for j in res[i].keys():
            if type(res[i][j])==type(datetime.now()):
                res[i][j] = res[i][j].strftime("%Y-%m-%d %H:%M:%S")
    return str(res)

@app.route("/api/selectcount")
def selectCount():
    res = db.selectcount()
    res[9] = 0
    tmp = [key for key in res.keys()]
    for key in tmp:
        if key not in (2, 4, 5, 9):
            res[9] += res[key]
            del res[key]
    tmp = [key for key in res.keys()]
    for key in tmp:
        res[str(key)] = res[key]
        del res[key]
    return str(res)

@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    tar = filename
    tar = int(tar)
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    )
    cursor = connection.cursor()
    cursor.execute("select Url,StateMent from WebPage;")
    filename+=".txt"
    with open("doc/" + filename, "w") as f:
        for item in cursor:
            url = item['Url']
            statement = item['StateMent']/100
            if statement not in (2, 4, 5):
                statement = 9
            if statement == tar:
                f.write(url)
                f.write('\n')
    cursor.close()
    connection.close()
    directory = os.getcwd()
    return send_from_directory(directory+"/doc", filename, as_attachment=True)

if __name__=='__main__':
    with open("doc/2.txt", "w") as f:
        f.write("sss")