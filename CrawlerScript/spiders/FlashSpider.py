from ast import parse
from readline import parse_and_bind
from subprocess import call
from time import time
import pymysql
import scrapy
from CrawlerScript.entity import WebPage
from scrapy.linkextractors import LinkExtractor
import CrawlerScript.database as db
import time

class Flashpider(scrapy.Spider):
    # 爬虫名为 SudaIndexSpider
    name = 'FlashSpider'
    # 爬取 suda.edu.cn域名下的网站
    allowed_domains = [
        'suda.edu.cn'
    ]
    def spider_opened(self, spider):
        self.start=time.time()
        start_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start)) #转化格式
        self.stats.set_value('start_time', start_time, spider=spider)
    def spider_closed(self, spider, reason):
        self.end = time.time()
        finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.end)) #转化格式
        self.stats.set_value('finish_time', finish_time, spider=spider)
        self.stats.set_value('finish_reason', reason, spider=spider)

        #这是计算此时运行耗费多长时间，特意转化为 时:分:秒
        Total_time=self.end-self.start
        m, s = divmod(Total_time, 60)
        h, m = divmod(m, 60)
        self.stats.set_value('Total_time', "共耗时===>%d时:%02d分:%02d秒" % (h, m, s), spider=spider)
    def db_url(self):
        # 临时游标
        tmpcursor = db.connection.cursor()
        # 访问数据库并且返回数据总量
        db.select_all_WebPage_Url(tmpcursor)
        # 进行迭代器遍历
        i = 0
        for url in tmpcursor:
            i += 1
            yield i,url['Url']
        # 关闭临时游标
        tmpcursor.close()
        return -1,-1

    # 初始函数
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        # 本爬虫的游标
        self.cursor = db.connection.cursor()

    def start_requests(self):
        # 遍历每一条数据
        for id, url in self.db_url():
            print(id,end = "\r")
            if id == -1:
                return
            # 剔除冗余数据
            # 尝试进行一次访问
            yield scrapy.Request(url,
                                dont_filter=False)
    def parse(self, response, **kwargs):
        pass