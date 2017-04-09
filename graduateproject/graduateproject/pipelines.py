# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
# import MySQLdb
# import MySQLdb.cursors
# from scrapy.exceptions import DropItem
# from twisted.enterprise import adbapi
# from scrapy import log


class GraduateprojectPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        url_address = dict(item)
        self.post.insert(url_address)
        return item
    # def __init__(self, dbpool):
    #     self.dbpool = dbpool
    #
    # @classmethod
    # def from_settings(cls, settings):
    #     dbargs = dict(
    #         host=settings['MYSQL_HOST'],
    #         db=settings['MYSQL_DBNAME'],
    #         user=settings['MYSQL_USER'],
    #         passwd=settings['MYSQL_PASSWD'],
    #         charset='utf8',
    #         cursorclass=MySQLdb.cursors.DictCursor,
    #         use_unicode=True,
    #     )
    #     dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
    #     return cls(dbpool)
    #
    # def process_item(self, item, spider):
    #     d = self.dbpool.runInteraction(self.__do__insert, item, spider)
    #     d.addBoth(lambda _: item)
    #     return d
    #
    # def __do__insert(self, conn, item, spider):
    #     try:
    #         conn.execute('insert INTO K_SITE_PIC_URLS VALUES (\'%s\')' % item['url_address'])
    #
    #     except MySQLdb.Error, e:
    #         spider.log("Mysql Error %d: %s" % (e.args[0], e.args[1]), level=log.DEBUG)
