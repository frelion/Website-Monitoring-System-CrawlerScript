# from subprocess import call
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# sudaLinksSet = set()
# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'https://www.suda.edu.cn/',
#     ]

#     def parse(self, response):
#         link_extractor = LinkExtractor(allow=(r'.*suda.*',), )
#         print('#'*30,'#'*30)
#         links = link_extractor.extract_links(response)
#         for link in links:
#             next_url = response.urljoin(link.url)
#             if next_url not in sudaLinksSet:
#                 sudaLinksSet.add(next_url)
#                 yield scrapy.Request(next_url, callback=self.parse)
#                 print(next_url)
        # print('#'*30,'#'*30)


import scrapy
from scrapy.linkextractors import LinkExtractor
sudaLinksSet = set()
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.suda.edu.cn/',
    ]

    def parse(self, response):
        link_extractor = LinkExtractor(allow=(r'.*suda.*',), )
        print('#'*30,'#'*30)
        print(response)
        links = link_extractor.extract_links(response)
        for link in links:
            next_url = response.urljoin(link.url)
            if next_url not in sudaLinksSet:
                sudaLinksSet.add(next_url)
                yield scrapy.Request(next_url, callback=self.parse)
                print(next_url)
        print('#'*30,'#'*30)







# http://tecj.suda.edu.cn/tcms/post/download?id=21052