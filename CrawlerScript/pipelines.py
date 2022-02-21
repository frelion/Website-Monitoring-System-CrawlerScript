# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from http.client import ImproperConnectionState
from bcrypt import re
from itemadapter import ItemAdapter
from .spiders.suda_index_spider import SudaIndexSpider
from .items import *
import CrawlerScript.database as db
from CrawlerScript.entity import WebPage

# 获取数据库游标
cursor = db.connection.cursor()


class CrawlerscriptPipeline:
    def open_spider(self, spider):
        pass
    def process_item(self, item, spider):
        return item


class SudaIndexSpiderPipeline:
    def process_item(self, item, spider):
        print('$'*100)
        if isinstance(item, WebPageItem) and isinstance(spider, SudaIndexSpider):
            # 插入数据
            db.insert_WebPage(spider.cursor, WebPage(item))
            pass
        else: return item