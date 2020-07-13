import requests
from bs4 import BeautifulSoup
import re


class SteamGameInfo:
    def __init__(self):
        self.session = requests.Session()

    def get_game_html(self, url):
        try:
            r = self.session.get(url)
            r.raise_for_status()
            return r.content
        except requests.exceptions.HTTPError as err:
            print('error: ', err)

    def strip_features(self, html):
        # object to return
        game = {}

        # turn the html into a searchable soup object
        soup = BeautifulSoup(html)
        tags = [tag.get_text().strip()
                for tag in soup.find_all('a', class_='app_tag')]
        # detail containers
        details = soup.find('div', class_='details_block')
        if details:
            details = details.get_text()
            game['Franchise'] = self.__re_detail('franchise', details)
            game['Genres'] = self.__re_detail('genre', details)

        cost_details = soup.find('div', class_='game_purchase_action')
        if cost_details:
            game['OriginalCost'], game['DiscountedCost'] = self.__get_prices(
                cost_details)

        game_details = soup.find_all('div', class_='game_area_details_specs')
        if game_details and tags:
            game['Players'] = self.__get_players(game_details, tags)
            game['Controller'] = self.__get_controller(game_details)

        language_details = soup.find('table', class_='game_language_options')
        if language_details:
            game['Languages'] = self.__get_languages(language_details)

        game['SteamURL'] = soup.find('div', class_='breadcrumbs')
        if game['SteamURL']:
            game['SteamURL'] = game['SteamURL'].find_all('a')[-1].get('href')
        if tags:
            game['Indie'] = 'Indie' in tags
            game['Soundtrack'] = 'Soundtrack' in tags

        # system requirements
        sys_requirements = soup.find('div', 'sysreq_contents')
        if sys_requirements:
            sys_requirements = self.__parse_sys_reqs(sys_requirements)

            game['Graphics'] = self.__get_graphics(sys_requirements)
            game['Storage'] = self.__get_storage(sys_requirements)
            game['Memory'] = self.__get_memory(sys_requirements)

        game['Tags'] = ', '.join(tags)

        return game

    def __re_detail(self, detail, text):
        '''Get the value after 'Detail: ' type string'''
        expression = f'{detail.title()}:[\\s\n].*'
        return re.search(expression, text).group().split(':')[1].strip()

    def __get_prices(self, details):
        discounted = details.find(
            'div', 'discount_block game_purchase_discount')
        if discounted:
            discounted_cost = discounted.find(
                'div', 'discount_final_price').text.strip()
            original_cost = discounted.find(
                'div', 'discount_original_price').text.strip()
        else:
            discounted_cost = None
            original_cost = details.find(
                'div', 'game_purchase_price price')
            if original_cost:
                original_cost = original_cost.text.strip()

        return original_cost, discounted_cost

    def __get_players(self, details, tags):
        player_choices = ['singleplayer', 'multiplayer', 'pvp', 'online pvp',
                          'lan pvp', 'shared/split screen pvp', 'coop',
                          'online coop', 'lan coop',
                          'shared/split screen coop',
                          'shared/split screen',
                          'crossplatform multiplayer']

        details = [detail.get_text().lower().replace('-', '').split(' ')
                   for detail in details]
        tags = [tag.lower().replace('-', '') for tag in tags]
        details += tags
        players = [choice for choice in player_choices if choice in details]
        return ', '.join(players)

    def __get_controller(self, details):
        all_details_text = [detail.get_text().lower().replace('-', '')
                            for detail in details]
        return 'controller' in ' '.join(all_details_text)

    def __get_languages(self, details):
        languages = [detail.get_text().strip()
                     for detail in details.find_all('td')]
        languages = [language for language in languages if language.isalpha()]
        return ', '.join(languages)

    def __parse_sys_reqs(self, sys_reqs):
        sys_reqs = sys_reqs.find_all('li')
        sys_reqs = [req.get_text() for req in sys_reqs]
        return ', '.join(sys_reqs)

    def __get_graphics(self, sys_reqs):
        gpu = self.__re_detail('Graphics', sys_reqs)
        gpu = self.__truncate_feature(gpu)
        return gpu

    def __get_storage(self, sys_reqs):
        storage = self.__re_detail('Storage', sys_reqs)
        if storage:
            storage = self.__truncate_feature(storage)
            return storage
        else:
            hard_drive = self.__re_detail('Hard Drive', sys_reqs)
            hard_drive = self.__truncate_feature(hard_drive)
            return hard_drive

    def __get_memory(self, sys_reqs):
        memory = self.__re_detail('Memory', sys_reqs)
        memory = self.__truncate_feature(memory)
        return memory

    def __truncate_feature(self, feature):
        if feature:
            comma_idx = feature.find(',')
            return feature[:comma_idx]
