# -*- coding: utf-8 -*-

# Scrapy settings for spiderzero project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spiderzero'

SPIDER_MODULES = ['spiderzero.spiders']
NEWSPIDER_MODULE = 'spiderzero.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spiderzero (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'spiderzero.middlewares.SpiderzeroSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'spiderzero.middlewares.SpiderzeroDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'spiderzero.pipelines.SpiderzeroPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

RANDOM_UA_TYPE = 'random'##random    chrome

DOWNLOADER_MIDDLEWARES = {

'spiderzero.Middlewares.user_agent_middlewares.RandomUserAgentMiddlware': 543, 

'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None

#'spiderzero.Middlewares.ip_pool.Ip_Pool':125,

#'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':543
}

COOKIES_ENABLED = True

DOWNLOAD_DELAY = 3

CONCURRENT_REQUESTS = 100

RETRY_ENABLED = False

DOWNLOAD_TIMEOUT = 15

CONCURRENT_REQUESTS_PER_SPIDER = 50

CONCURRENT_ITEMS = 200

CONCURRENT_REQUESTS_PER_DOMAIN = 64

REACTOR_THREADPOOL_MAXSIZE = 60


ITEM_PIPELINES = {
    'spiderzero.pipelines.WriteToCsv':300,
}


FEED_EXPORTERS = {                                                        
    'csv': 'spiderzro.spiders.csv_item_exporter.MyProjectCsvItemExporter',   
}    
                                                                          
FIELDS_TO_EXPORT = [                                                                                                                         
    'address',                                                             
    'areas',                                                              
    'build_year',                                                                
    'houseInfo',                                                              
    'level',                                                           
    'rooms',                                                              
    'totalPrice',
    'unitPrice'                                                             
] 


