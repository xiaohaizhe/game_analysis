# -*- coding: utf-8 -*-
from game_analysis.items import Game, Odds
from game_analysis.DBHelper import DBHelper


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class GameAnalysisPipeline(object):
    def process_item(self, item, spider):
        return item


class GamePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Game):
            db = DBHelper()
            db.insert_game(item)
        return item


class OddsPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Odds):
            db = DBHelper()
            db.insert_odds(item)
        return item
