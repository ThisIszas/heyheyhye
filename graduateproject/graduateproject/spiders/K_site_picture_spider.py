# coding:utf-8
import insert_to_SQL
import random
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
import re
import time
from scrapy.http import Request
from graduateproject.items import GraduateprojectItem
from termcolor import colored, cprint


class PicSpider(RedisSpider):
    def __init__(self, **kwargs):
        self.crawl_count = 1
        self.sensitive_words = ['breasts', 'censored', 'anus', 'uncensored', 'penis',
                                'pussy', 'nopan', 'cum', 'ass', 'anal', 'nude', 'sex', 'spread_legs', 'nipples',
                                'blush', 'wet', 'no bra', 'open_shirt', 'fingering', 'panties', 'panty_pull', 'yuri',
                                '2girls', 'cropped', 'underwear']
        super(PicSpider, self).__init__(**kwargs)

        self.save_tools = insert_to_SQL.SaveInfo()

    name = 'kSitePicSpider'
    start_urls = ['http://konachan.com/post?page=23&amp;tags=']
    redis_key = 'k_site_pic_spider:start_urls'

    def parse(self, response):
        # print response.body  # 源码
        print 'Now is crawl on page: ' + response.url
        print
        selector = Selector(response)
        all_pic_urls = selector.xpath('//body/div[@id="content"]/div[@id="post-list"]/div[@class="content"]'
                                      '/div/ul[@id="post-list-posts"]/li/div/a/@href').extract()
        print 'The amount of picture on this page is: ' + str(len(all_pic_urls))
        next_page_url = re.findall('next\" href=\"(.*?)\"', response.body, re.S)
        for e in next_page_url:
            print e

        for each in all_pic_urls:
            """
            This is the sample of each: '/post/show/239614/alicia_-granblue_fantasy-breasts-cait-gloves-granb'
            """
            temp_urls = 'http://konachan.com' + each
            yield Request(temp_urls, callback=self.parse_content)

        if next_page_url:
            print 'Start crawl next page.'
            """
            This is the sample of next_page_url[0]: '/post?page=3&amp;tags='
            """
            interval_time = random.uniform(2, 5)
            time.sleep(interval_time)
            real_next_page_url = 'http://konachan.com' + next_page_url[0]
            print 'Next page url is: ' + real_next_page_url
            yield Request(real_next_page_url, callback=self.parse)

    def parse_content(self, response):
        sensitive_word_appear_time = 0
        item = GraduateprojectItem()
        selector = Selector(response)
        tags = selector.xpath('//body//div[@id="content"]/div[@id="post-view"]/div[@class="sidebar"]'
                              '/div/ul[@id="tag-sidebar"]/li/@data-name').extract()
        tag_lens = len(tags)
        print "tag length is:" + str(tag_lens)
        for each in tags:
            # print each
            if each == ('nipples' or 'sex'):
                print 'sensitive_words is: ' + each
                # print '\t\t\tThis picture is passed\n'
                cprint('\t\t\tThis picture is passed\n', 'green', 'on_red')
                print response.url
                self.save_tools.insert_passed_info(response.url)
                print
                return

            elif each in self.sensitive_words:
                print 'sensitive_words is: ' + each
                print '\t\tdetected sensitive words'
                print "\t\tWarning: This picture may not satisfied."
                sensitive_word_appear_time += 1
                if sensitive_word_appear_time >= 4:
                    cprint('\t\t\tThis picture is passed\n', 'green', 'on_red')
                    print response.url
                    self.save_tools.insert_passed_info(response.url)
                    print
                    return
        if sensitive_word_appear_time == tag_lens:
            cprint('\t\t\tThis picture is passed\n', 'green', 'on_red')
            print response.url
            self.save_tools.insert_passed_info(response.url)
            print
            return

        real_pic_urls = selector.xpath('//body//div[@id="content"]/div[@id="post-view"]'
                                       '/div[@id="right-col"]/div/img/@src').extract()[0]
        """
        This is the sample of real_pic_urls: '//konachan.com/sample/4078e1c671f280d7569795cfa6de8f76
                                            /Konachan.com%20-%20239609%20sample.jpg'
        """
        real_pic_urls = 'http:' + real_pic_urls
        """
        This is the sample of final real_pic_urls: 'http://konachan.com/sample/4078e1c671f280d7569795cfa6de8f76
                                                    /Konachan.com%20-%20239609%20sample.jpg'
        """
        print 'The real pic adress is: ' + real_pic_urls
        if sensitive_word_appear_time == 3:
            self.save_tools.insert_questionable_info(real_pic_urls)
            print '\t\t\tThis picture is questionable\n'
            return

        self.save_tools.insert_info(real_pic_urls)
        item['url_address'] = real_pic_urls
        interval_time = random.uniform(2, 5)
        time.sleep(interval_time)
        print 'The number of picture is: ' + str(self.crawl_count)
        self.crawl_count += 1
        yield item
