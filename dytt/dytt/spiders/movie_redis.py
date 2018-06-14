# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_redis.spiders import RedisCrawlSpider
from dytt.items import DyttItem

class MovieSpider(RedisCrawlSpider):
    # name = 'movie'
    # allowed_domains = ['www.dytt8.net']
    # start_urls = ['http://www.dytt8.net/html/gndy/dyzz/list_23_1.html']
    name = 'myspider_redis'
    redis_key = 'myspider:start_urls'

    def parse(self, response):
        item = DyttItem()
        table_list = response.xpath("//table[@class='tbspan']")
        #获取最大页数
        page = re.compile(r'共(\d+)页')
        max_page = int(page.findall(response.text)[0])
        #解析页面
        for table in table_list:
            item['title'] = table.xpath(".//a/text()")[0].extract()
            item['brief'] = table.xpath(".//tr[last()]/td/text()")[0].extract()
            item['link'] = 'http://www.dytt8.net' + table.xpath(".//a/@href")[0].extract()
            # print(item)
            yield  scrapy.Request(item['link'], meta={'item': item}, callback=self.parse_detail)

        for i in range(2, max_page+1):
            url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'.format(i)
            yield scrapy.Request(url, callback=self.parse)

    #回调函数解析2级页面
    def parse_detail(self, response):
        item = response.meta['item']
        item['poster'] = response.xpath('//div[@id="Zoom"]//img[1]/@src')[0].extract()
        item['download_url'] = response.xpath('//div[@id="Zoom"]//table[1]//a/text()').extract()
        print(item)
        yield item