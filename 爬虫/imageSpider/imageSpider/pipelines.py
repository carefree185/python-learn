# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class ImagespiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """
        对媒体资源发起请求
        """
        yield scrapy.Request(item['image_url'])

    def file_path(self, request, response=None, info=None, *, item=None):
        """
        返回媒体资源的文件名
        :param request:
        :param response:
        :param info:
        :param item:
        :return:
        """
        return request.url.split('/')[-1]

    def item_completed(self, results, item, info):
        """
        将item提交给下一个管道类
        :param results:
        :param item:
        :param info:
        :return:
        """
        return item
