# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FirstbloodPipeline:
    fp = None

    def open_spider(self, spider):
        """
        该方法只会在爬虫执行时打开一次
        :param spider:
        :return:
        """
        self.fp = open('file.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        title = item['title']
        self.fp.write(title+'\n')
        return item  # 提交给下一个pipeline执行

    def close_spider(self, spider):
        """
        该方法只会在爬虫结束时调用一次
        :param spider:
        :return:
        """
        self.fp.close()
