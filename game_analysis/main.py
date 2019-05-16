import time
import os

while True:
    os.system("scrapy crawl spider_trade")
    # time.sleep(86400)  #每天一次 24*60*60=86400s
    time.sleep(3600)  # 每小时一次 60*60=3600s