# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.conf import settings
import pymysql

# class DushuPipeline(object):
#     def __init__(self):
#         self.fp = open("./novel.txt",'w', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         self.fp.write(json.dumps(dict(item), ensure_ascii=False) + '\n')
#         return item
#
#     def __del__(self):
#         self.fp.close()

# MYSQL_HOST = 'localhost'
# MYSQL_PORT = 3306
# MYSQL_DBNAME = 'books'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 199187
# CHARSET = 'utf8'

class DushuPipeline(object):
    def __init__(self):
        # settings =
        self.host = settings['MYSQL_HOST']
        self.port = settings['MYSQL_PORT']
        self.dbname = settings['MYSQL_DBNAME']
        self.user = settings['MYSQL_USER']
        self.password = settings['MYSQL_PASSWORD']
        self.charset = settings['CHARSET']
        self.conn = pymysql.connect(host = self.host, port = self.port, db = self.dbname,
                                  user = self.user, password = self.password, charset = self.charset)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        sql = "insert into book(name, author, brief) values('%s', '%s', '%s')" % (item['name'], item['author'], item['brief'])
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def __del__(self):
        self.conn.close()
