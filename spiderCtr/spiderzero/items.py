# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderzeroItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field() # 用于存储房子标题
    location = scrapy.Field() # 用于存储地理位置信息
    zone = scrapy.Field() # 用户存储房子的厅室信息
    meters = scrapy.Field() # 用于存储房子的平米信息
    direction = scrapy.Field() # 用于存储房子的朝向信息
    money = scrapy.Field() # 用于存储房子的月租信息
    pass
