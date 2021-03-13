import scrapy
from ..items import ImagespiderItem

class ImageSpider(scrapy.Spider):
    name = 'image'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://sc.chinaz.com/tupian/']
    url = "https://sc.chinaz.com/tupian/index_%d.html"

    def parse(self, response):
        div_list = response.xpath('//*[@id="container"]/div')
        for div in div_list:
            image_url = "https:" + div.xpath('./div/a/img/@src2').extract_first()
            item = ImagespiderItem()
            item['image_url'] = image_url
            yield item
