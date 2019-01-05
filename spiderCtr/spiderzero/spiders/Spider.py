# -*- coding: utf-8 -*-
import scrapy
from ..items import SpiderzeroItem
import time


class FinSpider(scrapy.Spider):
    name = "housespider"
    allowed_domains=["nj.lianjia.com"]
    start_urls = [
        "https://nj.lianjia.com/ershoufang"
    ]


    def start_requests(self):
        index = 1
        for index in range(5):
            url = self.start_urls[0] + '/pg' + str(index)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        time.sleep(2)
        item = SpiderzeroItem() 
        houses = response.xpath('//div[@class="info clear"]')
        for house in houses:
            item['community'] = house.xpath('./div[2]/div/a/text()').extract()[0].strip()
            item['houseInfo'] = house.xpath('./div[2]/div/text()').extract()[0].strip()
            item['positionInfo'] = house.xpath('./div[3]/div/a/text()').extract()[0].strip()
            item['followInfo'] = house.xpath('./div[4]/text()').extract()[0].strip()
            item['issubway'] = house.xpath('./div[5]/span[1]/text()').extract()[0].strip()
            item['totalPrice'] = house.xpath('./div[6]/div[1]/span/text()').extract()[0].strip()
            item['unitPrice'] = house.xpath('./div[6]/div[2]/span/text()').extract()[0].strip()
            print(item)
