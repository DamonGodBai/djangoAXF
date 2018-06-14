#!/usr/bin/python3
# -*- coding:utf-8 -*-

import redis
import pymysql
import json

def process_item():
    rediscli = redis.Redis(host='', port=6379, db=0)
    mysqlcli = pymysql.connect(host='', port='3306', user='',
                               pssswd='', db='')
    offset = 0
    while True:
        #将数据从redis中取出来
        source, data = rediscli.blpop('myspider:items')
        item = json.loads(data)
        cursor = mysqlcli.cursor()
        try:
            cursor.execute('insert into ')
            mysqlcli.commit()
        except:
            mysqlcli.rollback()
        finally:
            cursor.close()
        offset += 1


if __name__ == '__main__':
    process_item()