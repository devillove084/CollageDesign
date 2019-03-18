# -*- coding: utf-8 -*-
import scrapy
from ..items import SpiderzeroItem
import time
import json
import re
from lxml import etree
import urllib.request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError



class BeikeSpider(scrapy.Spider):
    name = "Beike"
    allowed_domains=["nj.ke.com"]
    base_url = 'https://nj.ke.com'
    fin_url = []
    start_urls = [
        "https://nj.ke.com/ershoufang/"
        #"https://nj.ke.com/chengjiao/"
    ]


    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url=url,callback=self.lv1_url,method='GET',
                            dont_filter=True,errback=self.errback_httpbin)

        #yield scrapy.Request(url=url, callback=self.parse,errback=self.errback_httpbin,
        #                        dont_filter=True)


    def lv1_url(self,response):
        t_url=[]
        for i in range(11):
            is_tr = response.xpath('//*[@id="beike"]/div[1]/div[3]/div[1]/dl[2]/dd/div[1]/div[1]/a[{}]/@href'.format(str(i+1)))
            if is_tr:
                t_url.append(is_tr.extract()[0].strip())
                url_tiny = self.base_url + str(t_url[i])
            i += 1

            yield scrapy.Request(url=url_tiny,callback=self.lv2_url,method='GET',
                                dont_filter=True,errback=self.errback_httpbin)


    def lv2_url(self,response):
        herf_url = response.xpath('//*[@id="beike"]/div[1]/div[3]/div[1]/dl[2]/dd/div[1]/div[2]/child::a/@href')
        for url in herf_url:
            l_url = self.base_url + str(url.extract().strip())
            
            def get_page_num(url):
                file = urllib.request.urlopen(url)
                res = file.read()
                selector = etree.HTML(res)
                pagecontent = selector.xpath('//div[@class="page-box house-lst-page-box"]')
                pages = 0
                if len(pagecontent):
                    pages = json.loads(pagecontent[0].xpath('./@page-data')[0]).get("totalPage")
                return pages
            
            page = get_page_num(l_url)
            for i in range(int(page)):
                url_page = l_url + 'pg{}'.format(str(i+1))
                yield scrapy.Request(url=url_page,callback=self.parse,method='GET',dont_filter=True,errback=self.errback_httpbin)
        



    def parse(self, response):
        item = SpiderzeroItem()
        houses = response.xpath('//li[@class="clear"]')
        for house in houses:
            item['houseInfo'] = house.xpath('./div/div[2]/div[1]/text()').extract()
            #item['houseInfo'] = re.findall(r'')
            item['positionInfo'] = house.xpath('./div/div[2]/div[2]/div/text()').extract()
            item['followInfo'] = house.xpath('./div/div[2]/div[3]/text()').extract()
            item['totalPrice'] = house.xpath('./div/div[2]/div[5]/div[1]/span/text()').extract()[0].strip()
            item['unitPrice'] = house.xpath('./div/div[2]/div[5]/div[2]/span/text()').extract()[0].strip()
            print(type(item['unitPrice']))
            yield item

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)