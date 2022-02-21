import time
from multiprocessing import  Process
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import flash.flash as flash
import flash.database as db
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def insertdb():
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res = db.selectcount()
    res[9] = 0
    tmp = [key for key in res.keys()]
    for key in tmp:
        if key not in (2, 4, 5, 9):
            res[9] += res[key]
            del res[key]
    sql = "INSERT INTO Log VALUES( '{}', {}, {}, {}, {} );".format(dt, res[2], res[4], res[5], res[9])
    print(sql)
    db.execute(sql)

@static_vars(cnt = 0)
def test(sched, repeats):
    test.cnt += 1
    print("俺开始执行了")
    # print()
    flash.flash(1<<12)
    print("开始写入Log数据库")
    insertdb()
    print("执行完毕")
    if test.cnt == repeats:
        print("俺要g了")
        sched.shutdown()

def run(task, repeats=-1, **kwargs):
    executors = {
    'default': ThreadPoolExecutor(40),
    'processpool': ProcessPoolExecutor(10)
    }
    sched = BlockingScheduler( executors=executors)
    print("已创建sched")

    time.sleep(1)

    sched.add_job(
        task, 
        'interval', 
        hours = kwargs.get('hours', 0), 
        minutes = kwargs.get('minutes', 0), 
        seconds = kwargs.get('seconds', 0), 
        start_date='2022-02-20 16:15:30', 
        args=[sched, repeats]
    )
    print("已装载函数")

    time.sleep(1)

    p = Process(target=sched.start)
    print("已创造新进程:", p)

    time.sleep(1)

    print("已启动进程")
    p.start()

    # 返回该进程
    return p


if __name__=='__main__':
    insertdb()
    # my_run = run
    # p = my_run(task = test, repeats = 3, minutes = 20)
    # print("返回的进程为:",p)
    # print("等待300000s")
    # time.sleep(300000)
    # p.terminate()
    # print("已终止进程")
    # time.sleep(5)
    # p.close()
    # print("进程关闭")