import scrapy
from selenium import webdriver
from ..items import NewsspiderItem


class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    model_url_list = []

    driver = webdriver.Chrome()

    def parse(self, response):
        # 解析出5个板块对应的url
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        index = [4, 5, 7, 8]
        for i in index:
            li = li_list[i]
            model_url = li.xpath('./a/@href').extract_first()
            self.model_url_list.append(model_url)
            yield scrapy.Request(model_url, callback=self.parse_model)

    def parse_model(self, response):
        # response对象此时是不符合需求的，由于获取的新闻是通过ajax加载出来的数据，要在中间件中拦截响应对象，并修改
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div/h3/a/text()').extract_first()
            detail_url = div.xpath('./div/div/h3/a/@href').extract_first()
            if not (title and detail_url):
                continue

            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={"title": title})

    def parse_detail(self, response):
        title = response.meta['title']
        detail = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        detail = ''.join(detail)
        item = NewsspiderItem()
        item['title'] = title
        item['detail'] = detail
        yield item

    def close(self, reason):
        self.driver.quit()
        super(NewsSpider, self).close(self, reason)
