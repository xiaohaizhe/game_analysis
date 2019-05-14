import time
import os

while True:
    os.system("scrapy crawl spider_trade")
    time.sleep(1800)  #每隔半个小时一次 30*60=1800s