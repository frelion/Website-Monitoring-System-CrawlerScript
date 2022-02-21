# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from typing import Counter
import scrapy


class CrawlerscriptItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WebPageItem(scrapy.Item):
    Url = scrapy.Field()
    StateMent = scrapy.Field()
    Count = scrapy.Field()