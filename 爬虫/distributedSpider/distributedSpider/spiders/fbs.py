import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from items import DistributedspiderItem


class FbsSpider(RedisCrawlSpider):
    name = 'fbs'
    redis_key = 'fbsQueue'
    rules = (
        Rule(LinkExtractor(allow=r'index[_0-9.]{1,}html'), follow=True),
        Rule(LinkExtractor(allow=r'/[0-9.]{1,}htm'), callback="parse_item")
    )

    def parse_item(self, response):
        image_url = "https:" + response.xpath('//div[@class="imga"]/a/@href').extract_first()
        item = DistributedspiderItem()
        item['image_url'] = image_url
        print(item)
        yield item
