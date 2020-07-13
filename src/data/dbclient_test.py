from dbclient import DBClient    
import unittest   
import os
import pandas as pd

class Test_DBClient(unittest.TestCase):
    def setUp(self):
        self.dbc = DBClient('test.db')

        self.mock_ideal_game = { 
            'Name': 'sample',
            'RawgID': 20, 
            'Metacritic': 100, 
            'Genres': 'Action', 
            'Indie': False,
            'Presence': 83, 
            'Platform': 'Windows', 
            'Graphics': '4gb GPU', 
            'Storage': '180gb',
            'Memory': '8gb',
            'RatingsBreakdown': '34/45/15', 
            'ReleaseDate': 'January 14, 2020', 
            'Soundtrack': False, 
            'Franchise': None,
            'OriginalCost': '$39.99', 
            'DiscountedCost': None, 
            'Players': 'singleplayer, multiplayer', 
            'Controller': True, 
            'Languages': 'English, Mandarin',
            'ESRB': 'Teen', 
            'Achievements': 55, 
            'Publisher': 'idSoftware', 
            'Description': 'lots of stuff',
            'Tags': 'Fun, Violent',
            'SteamURL': 'https://store.steampowered.com/app/42700/?snr=1_5_9__205', 
        }

    def tearDown(self):
        self.dbc.close()
        os.remove('test.db')

    def test_create_table(self):
        self.dbc.create_table()
        self.dbc.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        res = self.dbc.cursor.fetchall()
        self.assertIn(('games', ), res, 'game not found in tables')

    def test_drop_table(self):
        self.dbc.drop_table()
        self.dbc.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        res = self.dbc.cursor.fetchall()
        self.assertNotIn(('games', ), res, 'game not found in tables')

    def test_add_game(self):
        self.dbc.create_table()
        self.dbc.add_game(self.mock_ideal_game)
        self.dbc.cursor.execute("SELECT * FROM games")
        res = self.dbc.cursor.fetchone()
        self.assertIn(self.mock_ideal_game['SteamURL'], res, 'game with url not in table')

    def test_get_game(self):
        idx = 1
        self.dbc.create_table()
        self.dbc.add_game(self.mock_ideal_game)
        self.dbc.cursor.execute("SELECT id FROM games")
        res = [ features[0] for features in self.dbc.cursor.fetchall() ]
        self.assertIn(idx, res, 'game with idx no in table')
        game = self.dbc.get_game(idx)
        self.assertIs(game[0], idx, 'game idx does not match')

    def test_get_game_by_url(self):
        url = self.mock_ideal_game['SteamURL']
        self.dbc.create_table()
        self.dbc.add_game(self.mock_ideal_game)
        self.dbc.cursor.execute("SELECT SteamURL FROM games;")
        res = [ features[0] for features in self.dbc.cursor.fetchall() ]
        self.assertIn(url, res, 'game with url not in table')
        game = self.dbc.get_game_by_url(url)
        self.assertIn(url, game, 'returned game url does not match')

    def test_get_all_games(self):
        self.dbc.create_table()
        num_games = 5
        for idx in range(num_games):
            self.dbc.add_game(self.mock_ideal_game)

        games = self.dbc.get_all_games()
        self.assertIs(num_games, len(games), 'returned game length should equal num_games')

    def test_to_csv(self):
        self.dbc.create_table()
        num_games = 5
        for idx in range(num_games):
            self.dbc.add_game(self.mock_ideal_game)

        self.dbc.to_csv('test.csv')
        test_csv_df = pd.read_csv('test.csv')
        self.assertIs(num_games, test_csv_df.shape[0], 'test csv should have num_games rows')
        os.remove('test.csv')

    def test_delete_game(self):
        self.dbc.create_table()
        delete_idx = 2
        num_games = 5
        for idx in range(num_games):
            self.dbc.add_game(self.mock_ideal_game)
        
        self.dbc.cursor.execute("SELECT id FROM games;")
        game_ids = [ result[0] for result in self.dbc.cursor.fetchall() ]
        self.assertIn(delete_idx, game_ids, 'no game present with delete_idx')

        self.dbc.delete_game(delete_idx)
        self.dbc.cursor.execute("SELECT id FROM games;")
        game_ids = [ result[0] for result in self.dbc.cursor.fetchall() ]
        self.assertNotIn(delete_idx, game_ids, 'game with delete_idx still present')



if __name__ == '__main__':
    unittest.main()

    