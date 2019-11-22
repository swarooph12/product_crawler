# -*- coding: utf-8 -*-

# Scrapy settings for product_info_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'product_info_crawler'

SPIDER_MODULES = ['product_info_crawler.spiders']
NEWSPIDER_MODULE = 'product_info_crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'product_info_crawler (+http://www.yourdomain.com)'
#USER_AGENT = 'Mozilla/5.0'
# More comprehensive list can be found at 
# http://techpatterns.com/forums/about304.html
USER_AGENT_LIST = [
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]
DOWNLOADER_MIDDLEWARES = {
         'product_info_crawler.middlewares.RandomUserAgentMiddleware': 400,
         'product_info_crawler.middlewares.ProxyMiddleware': 410,
         'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    # Disable compression middleware, so the actual HTML pages are cached
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# output data format
FEED_FORMAT = "csv"
FEED_URI = "tmp/%(name)s.csv"

# Enable logs to see scrapy logs in command line
LOG_ENABLED=True

# Max deptth to crawl
DEPTH_LIMIT=2
FEED_EXPORT_FIELDS=["product_name", "price", "product_rating","image_url"]
