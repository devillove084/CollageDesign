import scrapy
from ..items import  SpiderzeroItem
class LianjiaSpider(scrapy.spiders.Spider):
    name = 'LianjiaSpider' # 爬虫名称
    start_urls = [] # 存储爬虫URL
    for i in range(1,101):
        start_urls.append('https://bj.lianjia.com/zufang/pg'+str(i)) # 存储链家网北京租房信息前100页的URL
    allowed_domains = ["linajia.com"]

    def parse(self, response):
        item = SpiderzeroItem() # 定义item类的对象用于储存数据
        title_list = response.xpath("//li[@data-el='zufang']/div[2]/h2/a/text()").extract() # 获取所有获取租房标题
        location_list = response.xpath("//li[@data-el='zufang']/div[2]/div[1]/div[1]/a/span/text()").extract() # 获取所有房子地理位置
        zone_list = response.xpath("//li[@data-el='zufang']/div[2]/div[1]/div[1]/span[1]/span/text()").extract() # 获取所有房子厅室信息
        meters_list = response.xpath("//li[@data-el='zufang']/div[2]/div[1]/div[1]/span[2]/text()").extract() # 获取所有房子的平米
        direction_list = response.xpath("//li[@data-el='zufang']/div[2]/div[1]/div[1]/span[3]/text()").extract() # 获取所有房子朝向
        money_list = response.xpath("//li[@data-el='zufang']/div[2]/div[2]/div[1]/span/text()").extract() # 获取所有房子的月租
        for i, j, k, l, m, n in zip(title_list, location_list, zone_list, meters_list, direction_list, money_list): # 将每种信息组合在一起,并传给一个item
            item['title'] = i
            item['location'] = j
            item['zone'] = k
            item['meters'] = l
            item['direction'] = m
            item['money'] = n
            yield item