# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NoveItem


class ReadSpider(CrawlSpider):
    name = 'read'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1078.html']

    rules = (
        # Rule(LinkExtractor(allow=r'/book/1078.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/book/1078_\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item= NoveItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        li_list = response.xpath('//div[@class="bookslist"]/ul/li')
        for book in li_list:
            item['name'] = book.xpath('.//h3/a/text()').extract_first()
            item['author'] = book.xpath('.//p[1]/a/text()').extract_first(default='暂缺作者')
            item['brief'] = book.xpath('.//p[last()-1]/text()').extract_first()
            yield item





