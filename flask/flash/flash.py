import flash.readToFile as rf
import flash.request as request
import flash.database as db
import time

def flashBatch(dic):
    for url,statement in dic.items():
        db.update(url, statement)



def flash(batch,patch=-1):
    t0 = time.time()
    print("开始扫描数据库")
    rf.write()
    print("开始访问")
    t1 = time.time()
    count = 1
    for dic in request.request(batch,patch):
        print("开始写入")
        flashBatch(dic)
        print(count,"~",count+len(dic)-1," 写入完成\n耗时:",time.time()-t1)
        t1 = time.time()
        count = count + len(dic)
    print("总耗时:",time.time()-t0)
if __name__ == '__main__':
    flash(1<<12)