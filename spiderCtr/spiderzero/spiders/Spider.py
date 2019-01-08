# -*- coding: utf-8 -*-
import scrapy
from ..items import SpiderzeroItem
import time
import requests
import re


class FinSpider(scrapy.Spider):
    name = "housespider"
    allowed_domains=["nj.lianjia.com"]
    start_urls = [
        "https://nj.lianjia.com/ershoufang"
    ]
    def start_requests(self):
        index = 1
        for index in range(100):
            url = self.start_urls[0] + '/pg' + str(index)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        time.sleep(2)
        item = SpiderzeroItem() 
        houses = response.xpath('//div[@class="info clear"]')
        for house in houses:
            item['community'] = house.xpath('./div[2]/div/a/text()').extract()[0].strip()
            item['houseInfo'] = house.xpath('./div[2]/div/text()').extract()[0].strip()

            item['rooms'] = re.findall(r'\d室\d厅',item['houseInfo'])
            item['areas'] = re.findall(r'[0-9]+\.[0-9]+平米',item['houseInfo'])
            item['design'] = re.findall(r'[简装,毛坯,精装,其他]',item['houseInfo'])
            item['dirction'] = re.findall(r'[东,西,南,北]',item['houseInfo'])
            item['iselevator'] = re.findall(r'[^\d]电梯',item['houseInfo'])

            item['positionInfo'] = house.xpath('./div[3]/div/a/text()').extract()[0].strip()
            item['followInfo'] = house.xpath('./div[4]/text()').extract()[0].strip()

            item['issubway'] = house.xpath('./div[5]/span[1]/text()').extract()[0].strip()
            item['totalPrice'] = house.xpath('./div[6]/div[1]/span/text()').extract()[0].strip()
            item['unitPrice'] = house.xpath('./div[6]/div[2]/span/text()').extract()[0].strip()
            item['unitPrice'] = re.findall(r'[\d]',item['unitPrice'])
            item['unitPrice'] = list(map(lambda x:int(x), item['unitPrice']))
            item['unitPrice'] = int(''.join(map(str, item['unitPrice'])))
            yield item
