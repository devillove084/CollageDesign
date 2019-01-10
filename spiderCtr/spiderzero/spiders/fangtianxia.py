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
    allowed_domains=["nanjing.esf.fang.com"]
    start_urls = [
        "https://nanjing.esf.fang.com/"
    ]
    def start_requests(self):
        index = 1
        for index in range(2):
            url = self.start_urls[0] + '/pg' + str(index)
            yield scrapy.Request(url=url, callback=self.parse,errback=self.errback_httpbin,
                                    dont_filter=True)
    
    def parse_page(self,response):
        pass



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