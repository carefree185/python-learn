# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymysql
from  .logger import streamLogger


class HuyaspiderPipeline:
    """
    该pipeline用于将数据写入文件
    """
    fp = None
    huya_list = []

    def open_spider(self, spider):
        """
        打开文件
        :param spider:
        :return:
        """
        self.fp = open('huya.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        """
        具体存储数据的过程
        :param item:
        :param spider:
        :return:
        """
        title = item['title']
        anchor = item['anchor']
        hot = item['hot']
        dic = {"title": title, 'anchor': anchor, 'hot': hot}
        self.huya_list.append(dic)
        streamLogger.info(f"添加数据{dic}")
        return item

    def close_spider(self, spider):
        """
        关闭文件
        :param spider:
        :return:
        """
        json.dump(self.huya_list, self.fp, ensure_ascii=False)
        streamLogger.info(f'保存数据{self.huya_list}')
        self.fp.close()


class HuyaspiderMysqlPipeline:
    """
    该pipeline用于将数据写入mysql
    """
    connection = None
    cursor = None

    def open_spider(self, spider):
        """
        建立数据库链接，如果表不存在，则创建
        :param spider:
        :return:
        """
        db_config = {
            "host": '127.0.0.1',
            "port": 3306,
            'user': 'root',
            'password': 'dyp1996',
            'db': 'huya',
            'charset': 'utf8',
        }
        self.connection = pymysql.connect(**db_config)
        self.cursor = self.connection.cursor()
        # 创建表需要约定主键为自增长
        # sql = "create table if not exists huya(id int auto_increment primary key, title varchar(255), anchor varchar(255), hot varchar(255));"
        # self.cursor.execute(sql)

    def process_item(self, item, spider):
        """
        具体存储数据的过程
        :param item:
        :param spider:
        :return:
        """
        title = item['title']
        anchor = item['anchor']
        hot = item['hot']
        sql = 'insert into huya(title, anchor, hot) value(%s, %s, %s);'
        try:
            self.cursor.execute(sql, (title, anchor, hot))
            self.connection.commit()
            streamLogger.info(f"执行sql: {sql}, 插入数据为: [{title, anchor, hot}]")
        except Exception as e:
            self.connection.rollback()
            streamLogger.error(f"执行sql: {sql}, 插入数据为: [{title, anchor, hot}] 执行出错{e}")

        return item

    def close_spider(self, spider):
        """
        关闭数据库链接
        :param spider:
        :return:
        """
        self.cursor.close()
        self.connection.close()
