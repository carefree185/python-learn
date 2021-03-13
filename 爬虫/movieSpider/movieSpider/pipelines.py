# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class MoviespiderPipeline:
    fp = None
    data = []

    def open_spider(self, spider):
        self.fp = open('movie.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item

    def close_spider(self, spider):
        json.dump(self.data, self.fp, ensure_ascii=False)
        self.fp.close()
