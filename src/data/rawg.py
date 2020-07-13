import requests 
import json 
from bs4 import BeautifulSoup

class RAWG:
    def __init__(self):
        self.base_url = 'https://api.rawg.io/api'
        self.session = requests.Session()

    def get_game(self, name):
        game = {}

        id = self.__request_id(name)
        if not id:
            return game

        res = self.__request_game(id)
        
        game['Name'] = res['name']
        game['RawgID'] = res['id']
        game['Metacritic'] = res['metacritic']
        game['Presence'] = self.__parse_precense(res)
        game['Presence'] = self.__score_precense(game['Presence'])
        game['Platform'] = self.__parse_platforms(res['platforms'])
        game['RatingsBreakdown'] = self.__parse_ratings(res['ratings'])
        game['ReleaseDate'] = res['released']
        game['ESRB'] = self.__parse_esrb(res['esrb_rating'])
        game['Achievements'] = res['achievements_count']
        game['CreatorsCount'] = res['creators_count'] 
        game['Description'] = self.__parse_description(res['description'])
        
        return game

    def __request_id(self, name):
        params = { 'search': name }
        try:
            res = self.session.get(f'{self.base_url}/games', params=params)
            if res.content:
                res = json.loads(res.content)
                if len(res['results']):
                    return res['results'][0]['id']
        except:
            return None

    def __request_game(self, id):
        res = self.session.get(f'{self.base_url}/games/{id}')
        res = json.loads(res.content)
        return res
    
    def __parse_description(self, description):
        soup = BeautifulSoup(description)
        return soup.get_text()

    def __parse_precense(self, social_media):
        keys = [ 'reddit_count', 'twitch_count', 'youtube_count', 
                'reviews_text_count', 'ratings_count', 'suggestions_count']
        vals = []

        for key in keys:
            vals.append(social_media[key])
        return dict(zip(keys, vals))
            
    def __score_precense(self, precense):
        score = 0
        for site in precense:
            score += precense[site]
        return score

    def __parse_platforms(self, platforms):
        platforms = [ platform['platform']['name'] for platform in platforms ]
        return ', '.join(platforms )

    def __parse_ratings(self, ratings):
       shortened_ratings =  [ f"{rating['title']}: {rating['count']}" for rating in ratings ]
       return ', '.join(shortened_ratings)
    
    def __parse_esrb(self, esrb_rating):
        if esrb_rating:
            return esrb_rating['name']