# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re
from bilibili_gaoxiao.items import BilibiliGaoxiaoItem
import numpy as np
import pandas as pd
import json
import jsonpath
from fake_useragent import UserAgent
import random


class BilibiliSpiderSpider(scrapy.Spider):
    name = 'bilibili_spider'
    #allowed_domains = ['https://api.bilibili.com']
    allowed_domains = ['bilibili.com']
    #start_urls = ['https://api.bilibili.com/x/web-interface/newlist?rid=138&type=0&pn=1&ps=20',
    #             'https://api.bilibili.com/x/web-interface/newlist?rid=138&type=0&pn=2&ps=20']
    page_url1 = 'https://api.bilibili.com/x/web-interface/newlist?rid=138&type=0&pn='
    page_url2 = '&ps=20'
    start_urls = []
    ua = UserAgent()
    for offset in range(1, 59829):
        start_url = page_url1 + str(offset) + page_url2
        start_urls.append(start_url)

    def parse(self, response):
        src = response.text
        j = json.loads(src)
        jobs = j['data']['archives']
        for job in jobs:
            aid = jsonpath.jsonpath(job, '$..aid')[0]  # av号
            tname = jsonpath.jsonpath(job, '$..tname')[0]  # 类型(搞笑)
            title = jsonpath.jsonpath(job, '$..title')[0]  # 视频标题
            #desc = jsonpath.jsonpath(job, '$..desc')[0]  # 视频描述
            pubdate = jsonpath.jsonpath(job, '$..pubdate')[0]  # 视频上传时间
            dynamic = jsonpath.jsonpath(job, '$..dynamic')[0]  # tag
            height = jsonpath.jsonpath(job, '$..height')[0]  # 分辨率长
            width = jsonpath.jsonpath(job, '$..width')[0]  # 分辨率宽
            name = jsonpath.jsonpath(job, '$..name')[0]  # up用户名
            mid = jsonpath.jsonpath(job, '$..mid')[0]  # upid
            coin = jsonpath.jsonpath(job, '$..coin')[0]  # 硬币数量
            danmaku = jsonpath.jsonpath(job, '$..danmaku')[0]  # 弹幕数量
            favorite = jsonpath.jsonpath(job, '$..favorite')[0]  # 收藏数量
            like = jsonpath.jsonpath(job, '$..like')[0]  # 点赞数量
            share = jsonpath.jsonpath(job, '$..share')[0]  # 分享数量
            view = jsonpath.jsonpath(job, '$..view')[0]  # 播放数量
            duration = jsonpath.jsonpath(job, '$..duration')[0]  # 播放时间2
            av_url = 'https://www.bilibili.com/video/av' + str(aid).strip()

            item = BilibiliGaoxiaoItem()
            item['av_url'] = av_url
            item['tname'] = tname
            item['title'] = title
            #item['desc'] = desc
            item['pubdate'] = pubdate
            item['dynamic'] = dynamic
            item['height'] = height
            item['width'] = width
            item['name'] = name
            item['mid'] = mid
            item['coin'] = coin
            item['danmaku'] = danmaku
            item['favorite'] = favorite
            item['like'] = like
            item['share'] = share
            item['view'] = view
            item['duration'] = duration

            request = scrapy.Request(av_url,
                                     callback=self.parse_video,
                                     headers = {'User-Agent': self.ua.random,
                                                'accept': 'image/webp,*/*;q=0.8',
                                                'accept-language': 'zh-CN,zh;q=0.8',
                                                'referer': 'https://www.bilibili.com/'},
                                     meta={'item': item,
                                           'dont_redirect': True,
                                           'handle_httpstatus_list': [302]})
            yield request

    def parse_video(self, response):
        item = response.meta['item']
        src2 = str(response.text)
        timelength_re = re.compile('"timelength":(.*?),"accept_format')
        timelengthList = timelength_re.findall(src2)
        if len(timelengthList) != 1:
            timelength = 0
        else:
            timelength = timelengthList[0]

        alltag_re = re.compile('tag_name":"(.*?)","cover')
        alltagList = alltag_re.findall(src2)
        alltagStr = "#".join(alltagList)
        if alltagStr != '':
            alltag = alltagStr
        else:
            alltag = '无标签'

        fanfollow_re = re.compile('"fans":(.*?),"friend":(.*?),"attention":(.*?),')
        #fanfollow_re = re.compile('"fans":(.*?),"friend":(.*?),"attention":(.*?),"sign')
        fansfollowerList = fanfollow_re.findall(src2)
        if len(fansfollowerList) != 1:
            fans = 0
            friend = 0
            attention = 0
        else:
            fansfollower = fansfollowerList[0]
            fans = fansfollower[0]
            friend = fansfollower[1]
            attention = fansfollower[2]

        #item = BilibiliGaoxiaoItem()
        item['timelength'] = timelength
        item['alltag'] = alltag
        item['fans'] = fans
        item['friend'] = friend
        item['attention'] = attention

        yield item
    #pass
