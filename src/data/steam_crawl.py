import requests
from selenium import webdriver
import time
import random
from tqdm import tqdm
from dbclient import DBClient
from steam_game_info import SteamGameInfo
from rawg import RAWG
from bs4 import BeautifulSoup


class SteamCrawl:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'https://store.steampowered.com/search'
        self.base_url += '/?category1=998&supportedlang=english'
        self.urls = []
        self.dbc = DBClient('games.db')
        self.dbc.create_table()

    def crawl(self, fetch_urls=False):
        # get list of urls
        if fetch_urls:
            self.__download_urls_page_source()
            self.__parse_urls()
        else:
            self.__parse_urls()
        # loop through list
        for url in tqdm(self.urls):
            if self.__already_downloaded(url):
                return
            # get features for each url
            game = {}
            game.update(self.__get_steam_features(url))
            game.update(self.__get_rawg_features(url))
            # save features in db
            self.dbc.add_game(game)

        self.dbc.to_csv('games.csv')

        return 'finished'

    def __download_urls_page_source(self):
        self.browser = webdriver.Safari()
        self.browser.get(self.base_url)
        self.__short_pause()
        lastHeight = self.browser.execute_script(
            "return document.body.scrollHeight")
        while True:
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            self.__short_pause()
            newHeight = self.browser.execute_script(
                "return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
        self.__save_game_list_source()
        self.browser.close()

    def __parse_urls(self):
        html = self.__load_game_list_source()
        soup = BeautifulSoup(html)
        a_tags = soup.find('div', id='search_results').find_all('a')
        self.urls = [a_tag.get('href') for a_tag in a_tags]

    def __save_game_list_source(self):
        with open("game_list.html", "w") as f:
            f.write(self.browser.page_source)

    def __load_game_list_source(self):
        with open("game_list.html", "r") as f:
            game_list_source = f.read()
        return game_list_source

    def __short_pause(self):
        duration = random.uniform(0, 3)
        time.sleep(duration)

    def __already_downloaded(self, url):
        game = self.dbc.get_game_by_url(url)
        return game

    def __get_steam_features(self, url):
        sgi = SteamGameInfo()
        html = sgi.get_game_html(url)
        if html:
            features = sgi.strip_features(html)
            return features

    def __get_rawg_features(self, url):
        name = url.split('/')[5].replace('_', ' ')
        rawg = RAWG()
        features = rawg.get_game(name)
        return features
