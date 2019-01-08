from scrapy import cmdline 
cmdline.execute("scrapy crawl housespider -o info.csv -t csv".split())
