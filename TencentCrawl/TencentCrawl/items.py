# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位名
    position_name = scrapy.Field()
    # 详情连接
    position_link = scrapy.Field()
    # 职位类别
    position_type = scrapy.Field()
    # 招聘人数
    people_number = scrapy.Field()
    # 工作地点
    work_location = scrapy.Field()
    # 发布事件
    publish_times = scrapy.Field()


class PositionItem(scrapy.Item):
    # 职位职责
    position_zhize = scrapy.Field()
    # 职位要求
    position_yaoqiu = scrapy.Field()
