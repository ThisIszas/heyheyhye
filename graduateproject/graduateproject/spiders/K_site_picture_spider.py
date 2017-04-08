# coding:utf-8
import insert_to_SQL
import random
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
import re
import time
from scrapy.http import Request


class PicSpider(RedisSpider):
    def __init__(self):
        self.save_tools = insert_to_SQL.SaveInfo()

    name = 'kSitePicSpider'
    start_urls = ['http://konachan.com/post']
    redis_key = 'k_site_pic_spider:start_urls'

    def parse(self, response, pagenum=2):
        # print response.body  # 源码
        print 'Now is crawl on page: ' + response.url
        print
        selector = Selector(response)
        all_pic_urls = selector.xpath('//body/div[@id="content"]/div[@id="post-list"]/div[@class="content"]'
                                      '/div/ul[@id="post-list-posts"]/li/div/a/@href').extract()
        print 'The amount of picture on this page is: ' + str(len(all_pic_urls))
        next_page_url = re.findall('next\" href=\"(.*?)\"', response.body, re.S)

        for each in all_pic_urls:
            """
            This is the sample of each: '/post/show/239614/alicia_-granblue_fantasy-breasts-cait-gloves-granb'
            """
            temp_urls = 'http://konachan.com' + each
            yield Request(temp_urls, callback=self.parseContent)

        if next_page_url:
            """
            This is the sample of next_page_url[0]: '/post?page=3&amp;tags='
            """
            time.sleep(5)
            real_next_page_url = 'http://konachan.com' + next_page_url[0]
            print 'Next page url is: ' + real_next_page_url
            yield Request(real_next_page_url, callback=self.parse)

    def parseContent(self, response):
        selector = Selector(response)
        real_pic_urls = selector.xpath('//body//div[@id="content"]/div[@id="post-view"]'
                                       '/div[@id="right-col"]/div/img/@src').extract()[0]
        """
        This is the sample of real_pic_urls: '//konachan.com/sample/4078e1c671f280d7569795cfa6de8f76
                                            /Konachan.com%20-%20239609%20sample.jpg'
        """
        real_pic_urls = re.sub('//', '', real_pic_urls)
        real_pic_urls = 'http://' + real_pic_urls
        """
        This is the sample of final real_pic_urls: 'http://konachan.com/sample/4078e1c671f280d7569795cfa6de8f76
                                                    /Konachan.com%20-%20239609%20sample.jpg'
        """
        print 'The real pic adress is: ' + real_pic_urls
        self.save_tools.insert_info(real_pic_urls)
        time.sleep(2.3)
        print
