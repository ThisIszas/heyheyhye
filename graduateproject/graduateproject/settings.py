# -*- coding: utf-8 -*-

BOT_NAME = 'graduateproject'

SPIDER_MODULES = ['graduateproject.spiders']
NEWSPIDER_MODULE = 'graduateproject.spiders'

ITEM_PIPELINES = ['graduateproject.pipelines.GraduateprojectPipeline']  # config it yourself

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'graduateproject.middlewares.ProxyMiddleware': 100,
}


SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
REDIS_URL = None
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'test_232'
MONGODB_DOCNAME = 'pic_urls'
