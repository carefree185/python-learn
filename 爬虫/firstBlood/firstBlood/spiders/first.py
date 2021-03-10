import scrapy

from ..items import FirstbloodItem

class FirstSpider(scrapy.Spider):
    name = 'first'  # 爬虫文件的名称, 爬虫源文件的唯一标识
    # allowed_domains = ['www.baidu.com', 'www.sogo.com']  # 允许的域名, 通常进行注释
    start_urls = ['https://dig.chouti.com/']  # 起始的url列表, scrapy会自动的获取url发起请求

    # 解析响应数据
    # def parse(self, response):
    #     content = []
    #
    #     div_list = response.xpath('/html/body/main/div/div/div[1]/div/div[2]/div[1]/div')
    #     for div in div_list:
    #         title = div.xpath('./div/div/div/a/text()').extract_first()
    #         content.append({"title": title})
    #
    #     return content

    def parse(self, response):

        div_list = response.xpath('/html/body/main/div/div/div[1]/div/div[2]/div[1]/div')
        for div in div_list:
            title = div.xpath('./div/div/div/a/text()').extract_first()
            item = FirstbloodItem()  # 一个地下只能保存一次循环中的值
            # item.title = title  # 父类被重写，该方式被丢弃
            item['title'] = title  # 对象通过[]调用或设置属性。重写 __setitem__和__getitem__
            yield item  # 将item对象提交给管道
