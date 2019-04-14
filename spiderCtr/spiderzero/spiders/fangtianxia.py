# -*- coding: utf-8 -*-
import scrapy
from ..items import FangTianXiaItem
import time
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError



class FangtianxiaSpider(scrapy.Spider):
    name = "Fangtianxia"
    base_url = "https://nanjing.esf.fang.com/"
    allowed_domains=["nanjing.esf.fang.com"]
    start_urls = [
        "https://nanjing.esf.fang.com/"
    ]
    
    
    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url=url, callback=self.parse_page,errback=self.errback_httpbin,
                            dont_filter=True)
    
    def parse_page(self,response):
        t_url=[]
        for i in range(1,12):
            is_tr = response.xpath('//*[@id="kesfqbfylb_A01_03_01"]/ul/li[{}]/a/@href'.format(str(i))).extract()[0].strip()
            if is_tr:
                t_url.append(is_tr)
                url_tiny = self.base_url + str(t_url[i])

            yield scrapy.Request(url=url_tiny,callback=self.parse,method='GET',
                                dont_filter=True,errback=self.errback_httpbin)




    def parse(self, response):
        time.sleep(2)
        item = FangTianXiaItem() 
        
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