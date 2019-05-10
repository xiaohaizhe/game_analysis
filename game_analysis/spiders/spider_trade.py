# -*- coding: utf-8 -*-
import scrapy
import requests
from datetime import datetime

start = datetime.strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')


class SpiderTradeSpider(scrapy.Spider):
    name = 'spider_trade'
    allowed_domains = ['500.com']
    start_urls = ['https://www.500.com/']

    def parse(self, response):
        results = response.xpath("//ul[@class='lottery_box']//li[position()<3]//div[@class='sub_lottery']//a[1]")
        for result in results:
            link = result.xpath("./@href").extract_first()
            link = "https:" + link
            yield scrapy.Request(link, callback=self.parse_second)

    def parse_second(self, response):
        results = response.xpath("//tbody//tr[@class='bet-tb-tr']")
        item = {}
        for result in results:
            full_name = result.xpath(".//td[2]/a/@title").extract_first()
            abbreviation = result.xpath(".//td[2]/a/text()").extract_first()
            kick_off_time = result.xpath(".//td[3]/text()").extract_first()
            roles = result.xpath(".//td[4]/div/span/a/text()").extract()
            link = result.xpath(".//td[7]/a[3]/@href").extract_first()
            item["full_name"] = full_name
            item["abbreviation"] = abbreviation
            item["kick_off_time"] = datetime.strptime("2019-" + kick_off_time, '%Y-%m-%d %H:%M')
            item["host_team"] = roles[0]
            item["visiting_team"] = roles[1]
            fid = link.split("-")[1].split(".")[0]
            yield scrapy.Request(link, callback=self.parse_third, meta={"fid": fid})

    def parse_third(self, response):
        fid = response.meta["fid"]
        results = response.xpath("//div[@class='table_cont']//table//tr[@ttl='zy']")
        for result in results[0:5]:
            company = result.xpath("./td[2]//a/span[2]/text()").extract_first()
            id = result.xpath("./@id").extract_first()
            print(str(id))
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            delta = datetime.now() - start
            _ = delta.days * 24 * 60 * 60 + delta.seconds
            payload = {
                "fid": fid,
                "cid": str(id),
                "r": "1",
                "time": time,
                "type": "europe",
                "_": _
            }
            link = "http://odds.500.com/fenxi1/json/ouzhi.php"
            res = requests.get(link, params=payload)
            res = res.text.strip("\r\n\r\n\r\n")
            result2 = []
            if "[[" in res:
                results1 = res.split("[")
                for result in results1:
                    print(result)
                    if result == "":
                        continue
                    result = result.strip("],")
                    print(result)
                    result = result.split(",")
                    count = 0
                    for r in result :
                        if ":" in r:
                            r = datetime.strptime(r , "%Y-%m-%d %H:%M:%S")
                        else:
                            r = float(r)
                        result[count] = r
                        count += 1
                    result2.append(result)
            print(company)
            print(result2)
