# -*- coding: utf-8 -*-
import scrapy
import requests
from datetime import datetime
from game_analysis.items import Game, Odds
from game_analysis.utils import create_uid
from game_analysis.DBHelper import DBHelper

start = datetime.strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')


class SpiderTradeSpider(scrapy.Spider):
    name = 'spider_trade'
    allowed_domains = ['500.com']
    start_urls = ['https://www.500.com/']

    def parse(self, response):
        results = response.xpath("//ul[@class='lottery_box']//li[1]//div[@class='sub_lottery']//a[1]")
        for result in results:
            first_title = result.xpath("./text()").extract_first()
            print(first_title)
            link = result.xpath("./@href").extract_first()
            link = "https:" + link
            yield scrapy.Request(link, callback=self.parse_second)

    def parse_second(self, response):
        results = response.xpath("//tbody//tr[@class='bet-tb-tr']")
        item = {}
        for result in results:
            game = Game()
            full_name = result.xpath(".//td[2]/a/@title").extract_first()
            abbreviation = result.xpath(".//td[2]/a/text()").extract_first()
            kick_off_time = result.xpath(".//td[3]/text()").extract_first()
            roles = result.xpath(".//td[4]/div/span/a/text()").extract()
            link = result.xpath(".//td[7]/a[3]/@href").extract_first()
            game_id = create_uid()
            game['id'] = game_id
            game["full_name"] = full_name
            game["abbreviation"] = abbreviation
            game["kick_off_time"] = datetime.strptime("2019-" + kick_off_time, '%Y-%m-%d %H:%M')
            game["host_team"] = roles[0]
            game["visiting_team"] = roles[1]
            db = DBHelper()
            gid = db.query_game(game)
            if gid == '':
                yield game
            else:
                game_id = gid
            fid = link.split("-")[1].split(".")[0]
            # print(game)
            yield scrapy.Request(link, callback=self.parse_third, meta={"fid": fid,"game_id":game_id})

    def parse_third(self, response):
        fid = response.meta["fid"]
        game_id = response.meta["game_id"]
        results = response.xpath("//div[@class='table_cont']//table//tr[@ttl='zy']")
        for result in results[0:5]:
            company = result.xpath("./td[2]//a/span[2]/text()").extract_first()
            id = result.xpath("./@id").extract_first()
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
                    # print(result)
                    if result == "":
                        continue
                    result = result.strip("],")
                    # print(result)
                    result = result.split(",")
                    count = 0
                    for r in result :
                        if ":" in r:
                            r = datetime.strptime(r.strip('"') , "%Y-%m-%d %H:%M:%S")
                        else:
                            r = float(r)
                        result[count] = r
                        count += 1
                    result2.append(result)
            # print(company)
            # print(result2)
            for result in result2:
                odds = Odds()
                odds_id = create_uid()
                odds['id'] =  odds_id
                odds['company_name'] = company
                odds['odds_of_winning']=result[0]
                odds['odds_of_losing']=result[1]
                odds['odds_of_draw']=result[2]
                odds['update_time']=result[4]
                odds['return_rates']=result[3]
                odds['game_id'] = game_id
                db = DBHelper()
                oid = db.query_odd(odds)
                if oid == '':
                    yield odds

