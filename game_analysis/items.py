# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GameAnalysisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Game(scrapy.Item):
    id = scrapy.Field()
    # 比赛全称
    full_name = scrapy.Field()
    # 比赛简称
    abbreviation = scrapy.Field()
    # 开赛时间
    kick_off_time = scrapy.Field()
    # 主队
    host_team = scrapy.Field()
    # 客队
    visiting_team = scrapy.Field()


class Odds(scrapy.Item):
    id = scrapy.Field()
    # 赔率公司
    company_name = scrapy.Field()
    # 赢球赔率
    odds_of_winning = scrapy.Field()
    # 输球赔率
    odds_of_losing = scrapy.Field()
    # 平局赔率
    odds_of_draw = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()
    # 返还率
    return_rates = scrapy.Field()
    # 关联比赛id
    game_id = scrapy.Field()
