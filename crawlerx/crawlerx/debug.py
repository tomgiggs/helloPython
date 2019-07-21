#encoding=utf8
from scrapy import cmdline
cmd = 'scrapy crawl postspider'
cmdline.execute(cmd.split()) #为什么一直报错No module named settings，其他地方用的好好的啊


