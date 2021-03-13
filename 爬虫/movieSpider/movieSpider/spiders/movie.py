import scrapy
from ..items import MoviespiderItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    # allowed_domains = ['www.xxxx.com']
    start_urls = ['https://www.4567kan.com/index.php/vod/show/id/1.html']
    url = 'https://www.4567kan.com/index.php/vod/show/id/%d.html'
    page = 1

    def parse(self, response):
        print("正在爬取第%d页" % self.page)
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            title = li.xpath("./div[@class='stui-vodlist__box']/a/@title").extract_first()
            detail_url = "https://www.4567kan.com" + li.xpath("./div[@class='stui-vodlist__box']/a/@href").extract_first()

            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={"title": title})

        tail = response.xpath('/html/body/div[1]/div/ul/li[10]/a/@href').extract_first()
        tail = tail.split('/')[-1].split('.')[0]
        tail = int(tail)
        if self.page < tail:
            self.page += 1
            next_url = self.url % self.page
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = MoviespiderItem()
        title = response.meta['title']
        desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
        item['title'] = title
        item['desc'] = desc
        yield item

