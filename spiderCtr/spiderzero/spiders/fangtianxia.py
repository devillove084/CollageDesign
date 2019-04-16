# -*- coding: utf-8 -*-
import scrapy
from ..items import FangTianXiaItem
import time
import re
from lxml import etree
import urllib.request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError



class FangtianxiaSpider(scrapy.Spider):
    name = "Fangtianxia"
    base_url = "https://nanjing.esf.fang.com"
    allowed_domains=["nanjing.esf.fang.com"]
    start_urls = [
        "https://nanjing.esf.fang.com/"
    ]
    
    
    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url=url, callback=self.parse_area,errback=self.errback_httpbin,
                            dont_filter=True)
    
    def parse_area(self,response):
        t_url=[]
        for i in range(1,12):
            is_tr = response.xpath('//*[@id="kesfqbfylb_A01_03_01"]/ul/li[{}]/a/@href'.format(str(i))).extract()[0].strip()
            if is_tr:
                t_url.append(is_tr)
                url_tiny = self.base_url + str(t_url[i-1])

            yield scrapy.Request(url=url_tiny,callback=self.parse_page,method='GET',
                                dont_filter=True,errback=self.errback_httpbin)

    def parse_page(self, response):

        def get_page_num(url):
            #req = urllib.request.Request(url)
            with urllib.request.urlopen(url) as response:
                res = response.read()
                selector = etree.HTML(res)
                pagecontent = selector.xpath('//*[@id="list_D10_15"]/child::p/text()')
                print(pagecontent)
                page = re.findall(r'[0-9]',pagecontent)
                print(page)
                return page

        o_url = response.xpath('//*[@id="ri010"]/div[1]/ul/li[2]/ul/child::node()/a/@href')
        #print(type(o_url))
        for url in o_url:
            #print(url)
            l_url = self.base_url + str(url.extract())
            print(l_url)
            print('--++___++')
            page = get_page_num(l_url)
            for i in range(int(page)):
                url_page = l_url + 'i3{}'.format(str(i+1))
                yield scrapy.Request(url=url_page, callback=self.parse, method='GET', dont_filter=True, errback=self.errback_httpbin)


    def parse(self, response):
        time.sleep(2)
        item = FangTianXiaItem()
        houses = response.xpath('//*[@id="kesfqbfylb_A01_01_03"]')
        print(houses)


        
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