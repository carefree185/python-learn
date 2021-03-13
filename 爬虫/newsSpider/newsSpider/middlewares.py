# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse


class NewsspiderDownloaderMiddleware:

    def process_response(self, request, response, spider):
        if request.url in spider.model_url_list:
            driver = spider.driver
            driver.get(request.url)
            body = driver.page_source
            response = HtmlResponse(url=request.url, body=body, request=request, encoding='utf-8')
            return response
        return response
