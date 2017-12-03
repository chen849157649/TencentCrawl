# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from TencentCrawl.items import TencentcrawlItem, PositionItem


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=True),

        # 只是一个跳板,没有callback意味着follow默认为True,追踪链接
        # Rule(LinkExtractor(allow=r'start=\d+')),
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+'), callback='parse_position', follow=False),

    )

    def parse_item(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentcrawlItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract_first()
            item['position_link'] = node.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = node.xpath("./td[2]/text()").extract_first()
            item['people_number'] = node.xpath("./td[3]/text()").extract_first()
            item['work_location'] = node.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = node.xpath("./td[5]/text()").extract_first()

            yield item

    def parse_position(self, response):
        i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
        item = PositionItem()
        item['position_zhize'] = "".join(response.xpath("//ul[@class='squareli']")[0].xpath("./li/text()").extract())
        item['position_yaoqiu'] = "".join(response.xpath("//ul[@class='squareli']")[1].xpath("./li/text()").extract())

        yield item

