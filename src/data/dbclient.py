import sqlite3
from sqlite3 import OperationalError
import pandas as pd


class DBClient:
    def __init__(self, db_path):
        '''Simple interface for creating a game database'''
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE games
                (id integer primary key autoincrement, Name, RawgID,
                SteamURL, Metacritic, Genres, Indie,
                Presence, Platform, Graphics, Storage, Memory,
                RatingsBreakdown, ReleaseDate, Soundtrack, Franchise,
                OriginalCost, DiscountedCost, Players, Controller, Languages,
                ESRB, Achievements, Publisher, Description, Tags)''')
            self.conn.commit()
        except OperationalError as e:
            print(f'error creating table: {e}')

    def drop_table(self):
        self.cursor.execute('''DROP TABLE IF EXISTS games''')
        self.conn.commit()

    def add_game(self, game):
        game = (game.get('Name', None),
                game.get('RawgID', None),
                game.get('SteamURL', None),
                game.get('Metacritic', None),
                game.get('Genres', None),
                game.get('Indie', None),
                game.get('Presence', None),
                game.get('Platform', None),
                game.get('Graphics', None),
                game.get('Storage', None),
                game.get('Memory', None),
                game.get('RatingsBreakdown', None),
                game.get('ReleaseDate', None),
                game.get('Soundtrack', None),
                game.get('Franchise', None),
                game.get('OriginalCost', None),
                game.get('DiscountedCost', None),
                game.get('Players', None),
                game.get('Controller', None),
                game.get('Languages', None),
                game.get('ESRB', None),
                game.get('Achievements', None),
                game.get('Publisher', None),
                game.get('Description', None),
                game.get('Tags', None))

        self.cursor.execute('''INSERT INTO games(
                Name, RawgID, SteamURL, Metacritic, Genres, Indie,
                Presence, Platform, Graphics, Storage, Memory,
                RatingsBreakdown, ReleaseDate, Soundtrack, Franchise,
                OriginalCost, DiscountedCost, Players, Controller,
                Languages, ESRB, Achievements, Publisher,
                Description, Tags) VALUES(?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', game)
        self.conn.commit()

    def get_game_by_url(self, url):
        self.cursor.execute('SELECT * FROM games WHERE SteamURL=?', (url, ))
        res = self.cursor.fetchone()
        return res

    def get_game(self, gameId):
        t = (gameId,)
        self.cursor.execute('SELECT * FROM games WHERE id=?', t)
        res = self.cursor.fetchone()
        return res

    def get_all_games(self):
        self.cursor.execute('SELECT * FROM games')
        res = self.cursor.fetchall()
        return res

    def to_csv(self, path):
        temp_df = pd.read_sql_query('SELECT * FROM games', con=self.conn)
        temp_df.to_csv(path)

    def delete_game(self, gameId):
        t = (gameId, )
        self.cursor.execute('DELETE FROM games WHERE id=?', t)
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()
