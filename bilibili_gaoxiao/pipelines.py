# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
import pymysql.cursors
import logging
import time

class BilibiliGaoxiaoPipeline(object):
    def open_spider(self, spider):
        self.file = open('C:\\Users\\Administrator\\Desktop\\数据分析\\bilibili_gaoxiao.csv', 'wb')#Running time
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class BilibiliGaoxiaoPipelineMysql(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='bilibili',  # 数据库名
            user='root',  # 数据库用户名
            passwd='123456',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into bilibili.bilibiligaoxiao(
                bilibiligaoxiao.av_url, 
                bilibiligaoxiao.tname, 
                bilibiligaoxiao.title, 
                bilibiligaoxiao.pubdate,
                bilibiligaoxiao.dynamic, 
                bilibiligaoxiao.height, 
                bilibiligaoxiao.width, 
                bilibiligaoxiao.name, 
                bilibiligaoxiao.mid, 
                bilibiligaoxiao.coin, 
                bilibiligaoxiao.danmaku,
                bilibiligaoxiao.favorite,
                bilibiligaoxiao.like,
                bilibiligaoxiao.share,
                bilibiligaoxiao.view,
                bilibiligaoxiao.timelength,
                bilibiligaoxiao.alltag,
                bilibiligaoxiao.fans,
                bilibiligaoxiao.friend,
                bilibiligaoxiao.attention,
                bilibiligaoxiao.writetime,
                bilibiligaoxiao.flag,
                bilibiligaoxiao.duration)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (item['av_url'].strip('\n').strip(),
                 item['tname'].strip('\n').strip(),
                 item['title'].strip('\n').strip(),
                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['pubdate'])),
                 item['dynamic'].strip('\n').strip(),
                 item['height'],
                 item['width'],
                 item['name'].strip('\n').strip(),
                 item['mid'],
                 item['coin'],
                 item['danmaku'],
                 item['favorite'],
                 item['like'],
                 item['share'],
                 item['view'],
                 item['timelength'],
                 item['alltag'].strip('\n').strip(),
                 item['fans'],
                 item['friend'],
                 item['attention'],
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 11,
                 item['duration']))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            logging.log(error)
        return item  # 必须实现返回
