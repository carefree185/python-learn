import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import SuncrawlItem


class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://sc.chinaz.com/tupian/']

    rules = (
        Rule(LinkExtractor(allow=r'index_[0-9.]{1,}html'), follow=True),
        Rule(LinkExtractor(allow=r'/[0-9.]{1,}htm'), callback="parse_item")
    )

    def parse_item(self, response):
        image_url = "https:" + response.xpath('//div[@class="imga"]/a/@href').extract_first()
        item = SuncrawlItem()
        item['url'] = image_url
        yield item
