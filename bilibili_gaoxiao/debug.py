#!/usr/bin/python

from scrapy.cmdline import execute
import sys
import os
# __file__ :当前文件夹

# os.path.abspath: 文件的绝对路径

# os.path.dirname: 文件的上一级

# sys.path.append  插入到环境变量

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy', 'crawl', 'bilibili_spider'])
