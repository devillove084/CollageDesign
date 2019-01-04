# -*- coding: utf-8 -*-
import scrapy
import random


class FinSpider(scrapy.Spider):
    name = "housespider"
    allowed_domains=["nj.lianjia.com"]


    def start_requests(self):
        urls = [
            'https://nj.lianjia.com/ershoufang/sanpailou/',
            'https://nj.lianjia.com/ershoufang/hunanlu/',
        ]
        for url in urls:
            print(scrapy.Request)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'house%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        print('Saved file %s' % filename)