import pymysql
from game_analysis.utils import create_uid
from game_analysis.settings import host, port, user, password, db, charset


class DBHelper():
    def __init__(self) -> None:
        super().__init__()
        conn = pymysql.Connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=db,
            charset=charset)
        self.conn = conn

    def insert_game(self, item):
        cursor = self.conn.cursor()
        sql = "INSERT INTO game(id,full_name, abbreviation,kick_off_time,host_team, visiting_team)VALUES (%s, %s, %s,%s, %s, %s);"

        data = (item['id'], item['full_name'], item['abbreviation'], item['kick_off_time'], item['host_team'],
                item['visiting_team'])
        cursor.execute(sql, data)
        self.conn.commit()
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        self.conn.close()

    def query_game(self,item):
        cursor = self.conn.cursor()
        sql = "SELECT id FROM game WHERE full_name='%s' and host_team='%s' and visiting_team='%s' and kick_off_time = '%s'"
        data = (item['full_name'],item['host_team'],item['visiting_team'],item['kick_off_time'])
        cursor.execute(sql % data)
        game_id = ''
        # count = cursor.rowcount
        for row in cursor.fetchall():
            game_id = row[0]
        # 查出数据数量
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return game_id

    def insert_odds(self, item):
        cursor = self.conn.cursor()
        sql = "INSERT INTO odds(id,company_name, odds_of_winning,odds_of_losing,odds_of_draw, update_time," \
              "return_rates,game_id)VALUES (%s, %s, %s,%s, %s, %s, %s, %s);"
        odds_id = create_uid()
        data = (odds_id, item['company_name'], item['odds_of_winning'], item['odds_of_losing'], item['odds_of_draw'],
                item['update_time'], item['return_rates'], item['game_id'])
        cursor.execute(sql, data)
        self.conn.commit()
        cursor.close()
        self.conn.close()


    def query_odd(self,item):
        cursor = self.conn.cursor()
        sql = "SELECT id FROM odds WHERE company_name='%s' and update_time='%s' and game_id='%s'"
        data = (item['company_name'],item['update_time'],item['game_id'])
        cursor.execute(sql % data)
        odds_id = ''
        # count = cursor.rowcount
        for row in cursor.fetchall():
            odds_id = row[0]
        # 查出数据数量
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return odds_id
