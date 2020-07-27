from flask_restful import reqparse, Resource
import json
import sqlite3
from sqlite3 import OperationalError


class ListGames(Resource):
    def __init__(self):

        # setup the parser for getting args
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('score', type=float)
        self.parser.add_argument('amount', type=int)

    def get(self):
        # parse the args
        args = self.parser.parse_args()

        score = args['score']
        amount = args['amount']

        if score < 5:
            score = 5

        games = self.__get_games(score, amount)

        return {'games': json.dumps(games)}

    def __get_games(self, score, amount):
        min_id = score - (amount/2)
        max_id = score + (amount/2)
        games = []

        try:
            self.__init_db()
            q = '''
                SELECT id, name
                FROM games
                WHERE id BETWEEN ? AND ?
            '''
            self.cursor.execute(q, [min_id, max_id])
            games = self.cursor.fetchall()

        except OperationalError as e:
            print(f'error fetching games: {e}')
      
        self.__close_db()
        games = self.__parse_games(games)
        return games

    def __parse_games(self, games):
        return [dict(id=game[0], name=game[1]) for game in games]

    def __init_db(self):
        try:
            db_path = './data/games.db'
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except OperationalError as e:
            print('error opening db connection', e)
    
    def __close_db(self):
        try:
            self.conn.close()
        except OperationalError as e:
            print('error closing db', e)
