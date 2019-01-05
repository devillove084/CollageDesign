# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderzeroItem(scrapy.Item):
    houseInfo = scrapy.Field() # 用于存储房子标题
    community = scrapy.Field()
    positionInfo = scrapy.Field() # 用于存储地理位置信息
    followInfo = scrapy.Field() # 用户存储房子的厅室信息
    issubway = scrapy.Field() # 用于存储房子的平米信息
    totalPrice = scrapy.Field() # 用于存储房子的月租信息
    unitPrice = scrapy.Field()
    pass
