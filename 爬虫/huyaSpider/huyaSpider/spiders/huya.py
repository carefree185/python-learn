import scrapy
from ..items import HuyaspiderItem


class HuyaSpider(scrapy.Spider):
    name = 'huya'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.huya.com/g/wzry']
    url = "https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=2336&tagAll=0&page=%d"
    # def parse(self, response):
    #     li_list = response.xpath('//*[@id="js-live-list"]/li[position()>6]')
    #     for li in li_list:
    #         title = li.xpath('./a[2]/text()').extract_first()
    #         anchor = li.xpath("./span/span[1]/i[@class='nick']/text()").extract_first()
    #         hot = li.xpath('./span[@class="txt"]/span[@class="num"]/i[2]/text()').extract_first()
    #         item = HuyaspiderItem()
    #         item['title'] = title
    #         item['anchor'] = anchor
    #         item['hot'] = hot
    #         yield item

    def parse(self, response):
        li_list = response.xpath('//*[@id="js-live-list"]/li[position()>6]')
        for li in li_list:
            title = li.xpath('./a[2]/text()').extract_first()
            anchor = li.xpath("./span/span[1]/i[@class='nick']/text()").extract_first()
            hot = li.xpath('./span[@class="txt"]/span[@class="num"]/i[2]/text()').extract_first()
            item = HuyaspiderItem()
            item['title'] = title
            item['anchor'] = anchor
            item['hot'] = hot
            yield item

        for page in range(2,26):
            next_url = self.url % page
            yield scrapy.Request(next_url, callback=self.parse_other)  # 手动发起请求

    def parse_other(self, response):
        print(response.text)


