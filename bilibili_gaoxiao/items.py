# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliGaoxiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    av_url = scrapy.Field()  # av号
    tname = scrapy.Field()  # 类型(搞笑)
    title = scrapy.Field()  # 视频标题
    #desc = scrapy.Field()  # 视频描述
    pubdate = scrapy.Field()  # 视频上传时间
    dynamic = scrapy.Field()  # tag
    height = scrapy.Field()  # 分辨率长
    width = scrapy.Field()  # 分辨率宽
    name = scrapy.Field()  # up用户名
    mid = scrapy.Field()  # upid
    coin = scrapy.Field()  # 硬币数量
    danmaku = scrapy.Field()  # 弹幕数量
    favorite = scrapy.Field()  # 收藏数量
    like = scrapy.Field()  # 点赞数量
    share = scrapy.Field()  # 分享数量
    view = scrapy.Field()  # 播放数量
    duration = scrapy.Field()  # 视频时长2
    timelength = scrapy.Field()  # 视频时长
    alltag = scrapy.Field()  # 所有tag
    fans = scrapy.Field()  # 粉丝数量
    friend = scrapy.Field()  # 朋友数量
    attention = scrapy.Field()  # 关注数量


    pass
