# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from TencentCrawl.items import TencentcrawlItem, PositionItem


class TencentcrawlPipeline(object):
    def open_spider(self, spider):
        self.file = open('position_info.json', 'w')

    def process_item(self, item, spider):
        if isinstance(item, TencentcrawlItem):
            item = dict(item)
            content = json.dumps(item, ensure_ascii=False) + ',\n'
            self.file.write(content.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.file.close()


class PositionPipeline(object):
    def open_spider(self, spider):
        self.file = open('position_task.json', 'w')

    def process_item(self, item, spider):
        if isinstance(item, PositionItem):
            item = dict(item)
            content = json.dumps(item, ensure_ascii=False) + ',\n'
            self.file.write(content.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.file.close()