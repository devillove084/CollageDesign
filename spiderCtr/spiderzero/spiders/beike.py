# -*- coding: utf-8 -*-
import scrapy
from ..items import SpiderzeroItem
import time
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError



class BeikeSpider(scrapy.Spider):
    name = "Beike"
    allowed_domains=["nj.ke.com"]
    base_url = 'https://nj.ke.com'
    start_urls = [
        "https://nj.ke.com/ershoufang/"
        #"https://nj.ke.com/chengjiao/"
    ]


    def start_requests(self):
        index = 1
        for index in range(1):
            url = self.start_urls[0] + 'pg' + str(index)
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
            fin_url = self.base_url + str(url.extract().strip())
            yield scrapy.Request(url=fin_url,callback=self.parse,method='GET',dont_filter=True,errback=self.errback_httpbin)
        
        


    def parse(self, response):
        time.sleep(2)
        item = SpiderzeroItem()
        pagesize = response.xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[5]/div[2]/div/@page-data')
        #houses = response.xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[4]/ul')
        #for house in houses:
            #item['community'] = house.xpath('./li[1]/div/div[1]/a/text()').extract()[0].strip()
        item['houseInfo'] = pagesize
        #house.xpath('./li[1]/div/div[1]/a/text()').extract()[0].strip()

            #item['rooms'] = re.findall(r'\d室\d厅',item['houseInfo'])
            #item['areas'] = re.findall(r'[0-9]+\.[0-9]+平米',item['houseInfo'])
            #item['design'] = re.findall(r'[简装,毛坯,精装,其他]',item['houseInfo'])
            #item['dirction'] = re.findall(r'[东,西,南,北]',item['houseInfo'])
            #item['iselevator'] = re.findall(r'[^\d]电梯',item['houseInfo'])

            #item['positionInfo'] = house.xpath('./div[3]/div/a/text()').extract()[0].strip()
            #item['followInfo'] = house.xpath('./div[4]/text()').extract()[0].strip()

            #item['issubway'] = house.xpath('./div[5]/span[1]/text()').extract()[0].strip()
            #item['totalPrice'] = house.xpath('./div[6]/div[1]/span/text()').extract()[0].strip()
            #item['unitPrice'] = house.xpath('./div[6]/div[2]/span/text()').extract()[0].strip()
            #item['unitPrice'] = re.findall(r'[\d]',item['unitPrice'])
            #item['unitPrice'] = list(map(lambda x:int(x), item['unitPrice']))
            #item['unitPrice'] = int(''.join(map(str, item['unitPrice'])))

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