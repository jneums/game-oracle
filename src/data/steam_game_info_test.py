from steam_game_info import SteamGameInfo    
import unittest   


class Test_SteamGameInfo(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_something(self):
        pass

   

if __name__ == '__main__':
    unittest.main()


# instantiate
# s = SteamGameInfo()

# discounted_game_url = 'https://store.steampowered.com/app/447040/Watch_Dogs_2/'
# normal_game_url = 'https://store.steampowered.com/app/42700/Call_of_Duty_Black_Ops/'

# html = s.get_game_html(discounted_game_url)
# # html = s.get_game_html(normal_game_url)

# # pull features from html
# features = s.strip_features(html)
# features