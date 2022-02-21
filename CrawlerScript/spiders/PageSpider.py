from ast import parse
from readline import parse_and_bind
from subprocess import call
import pymysql
import scrapy
from CrawlerScript.entity import WebPage
from scrapy.linkextractors import LinkExtractor
import CrawlerScript.database as db

class PageSpider(scrapy.Spider):
    # 爬虫名为 SudaIndexSpider
    name = 'PageSpider'
    # 爬取 suda.edu.cn域名下的网站
    allowed_domains = [
        'suda.edu.cn'
    ]
    
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
        # 拿到数据库中所有数据的数量
        # cnt = self.db_url()

        # 遍历每一条数据
        for id, url in self.db_url():
            print(id, url)
            # 遍历到头了
            if id == -1:
                return
            # 剔除冗余数据
            if 'suda.edu.cn' not in url:
                db.delete_WebPage(self.cursor, url)
                print('删除数据!')
                continue
            # 尝试进行一次访问
            print('试图访问!')
            yield scrapy.Request(url,
                                errback=self.eBack,
                                callback=self.parse_db,
                                dont_filter=False)
 
    # 定义访问失败时的函数
    def eBack(self, failure):
        # 拿到访问失败的url
        targetUrl = failure.request.url
        # 查询数据库中是否已经存在本网站
        page = db.select_WebPage(self.cursor, targetUrl)

        # 如果不存在则插入进去
        if page == -1:
            web_page = WebPage(targetUrl, 2, 1)
            db.insert_WebPage(self.cursor, web_page)
            page = db.select_WebPage(self.cursor, targetUrl)[0]
        # 否则更新Count
        else :
            page = page[0]
            web_page = WebPage(targetUrl, 2, 1)
            if page['StateMent'] == 2:
                web_page = WebPage(targetUrl, 2, page['Count'] + 1)
            db.insert_WebPage(self.cursor, web_page)
            page = db.select_WebPage(self.cursor, targetUrl)[0]
        
        # 如果在允许的范围内则尝试重新访问
        # print('$'*20,'$'*20)
        # print(page)
        # print('$'*20,'$'*20)
        if page['Count'] <= 3:
            return scrapy.Request(targetUrl, 
                                    callback=self.parse_db,
                                    errback=self.eBack,
                                    dont_filter=True)
        # 负责直接输入不可访问,结束这一切
        else:
            print('访问失败!')
            web_page = WebPage(targetUrl, 0, 100)
            db.insert_WebPage(self.cursor, web_page)
            return
        
    def parse_db(self, response, **kwargs):
        print('访问成功!')
        # 访问成功将自己塞入管道之中，若数据库中已经存在就覆盖
        web_page = WebPage(response.url, 1, 0)
        db.insert_WebPage(self.cursor, web_page)

        # 如果是下载链接则不再搜索
        if 'text' not in str(response.headers['Content-Type']):
            return
        # 生成链接提取器，关键词为suda
        link_extractor = LinkExtractor(allow_domains='suda.edu.cn')
        # 提取所有含有suda关键词的链接
        links = link_extractor.extract_links(response)
        # 遍历每一个链接
        for link in links:
            # 利用response.urljjoin合并url，因为可能是相对位置
            next_url = response.urljoin(link.url)
            # 如果之前没有访问过，就访问,防止爬虫循环
            page = db.select_WebPage(self.cursor, next_url)
            if page == -1 or len(page) == 0:
                yield scrapy.Request(next_url,
                                    callback=self.parse_db,
                                    errback=self.eBack,
                                    dont_filter=False,)