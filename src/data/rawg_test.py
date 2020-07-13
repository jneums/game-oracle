from rawg import RAWG 
import unittest   


class Test_RAWG(unittest.TestCase):
    def setUp(self):
        self.rawg = RAWG()
        self.maxDiff = None

    def tearDown(self):
        pass
    
    def test_get_valid_game(self):
        test_title = 'bioshock'
        res = self.rawg.get_game(test_title)
        expected_game = {
            'Name': 'BioShock',
            'RawgID': 4286,
            'ReleaseDate': '2007-08-21'
        }
        self.assertIsInstance(res, dict, 'should return dict')
        self.assertDictContainsSubset(expected_game, res, 'name, rawgid, and release data should match')
   
    def test_get_invalid_game(self):
        test_title = ''
        res = self.rawg.get_game(test_title)
        expected_game = {}
        self.assertIsInstance(res, dict, 'response should be a dict')
        self.assertDictContainsSubset(expected_game, res, 'res should match expected')

if __name__ == '__main__':
    unittest.main()

    