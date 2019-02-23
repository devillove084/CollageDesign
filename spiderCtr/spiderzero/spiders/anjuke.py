# -*- coding: utf-8 -*-
import scrapy
from ..items import AnjukeItem
import time
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError



class AnjukeSpider(scrapy.Spider):
    name = "anjuke"
    allowed_domains=["nanjing.anjuke.com"]
    start_urls = [
        "https://nanjing.anjuke.com/sale"
    ]
    def start_requests(self):
        index = 1
        for index in range (100):
            url = self.start_urls[0] + '/p' + str(index)
            yield scrapy.Request(url=url, callback=self.parse,errback=self.errback_httpbin,
                                    dont_filter=True)



    def parse_page(self,response):

        pass


    i = 1
    def parse(self, response):
        time.sleep(2)
        item = AnjukeItem()
        houses = response.xpath('//*[@id="houselist-mod-new"]')
        #for i in range(1,10):
            #strr = '//*[@id="houselist-mod-new"]/li[' + str(i) + ']'
            #houses = response.xpath(strr)
        for house in houses:
            for i in range(1,100):
                strr = 'li[' + str(i) + ']'
                item['houseInfo'] = house.xpath('./{}/div[2]/div[1]/a/text()'.format(strr)).extract()[0].strip()
                item['rooms'] = house.xpath('./{}/div[2]/div[2]/span[1]/text()'.format(strr)).extract()[0].strip()
                item['areas'] = house.xpath('./{}/div[2]/div[2]/span[2]/text()'.format(strr)).extract()[0].strip()
                item['level'] = house.xpath('./{}/div[2]/div[2]/span[3]/text()'.format(strr)).extract()[0].strip()
                item['build_year'] = house.xpath('./{}/div[2]/div[2]/span[4]/text()'.format(strr)).extract()[0].strip()
                item['address'] = house.xpath('./{}/div[2]/div[3]/span/text()'.format(strr)).extract()[0].strip()
                #item['issubway'] = house.xpath('./div[2]/div[4]/span[1]/text()').extract()[0].strip()
                #item['isschool'] = house.xpath('./div[2]/div[4]/span[2]/text()').extract()[0].strip()
                item['totalPrice'] = house.xpath('./{}/div[3]/span[1]/strong/text()'.format(strr)).extract()[0].strip()
                item['unitPrice'] = house.xpath('./{}/div[3]/span[2]/text()'.format(strr)).extract()[0].strip()
                i = i+1
                print(i)
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