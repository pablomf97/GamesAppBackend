from bs4 import BeautifulSoup
import requests

from game.models import ListGame, Game

from ..utils.utils import *

REQUEST_URL_BASE = 'https://www.allkeyshop.com/blog/'
REQUEST_URL_SEARCH = REQUEST_URL_BASE + 'catalogue/search-'


def get_top_25():
    # Get the top 25 games
    html_text = requests.get(REQUEST_URL_BASE).text
    # Create the soup
    soup = BeautifulSoup(html_text, 'lxml')

    # Mess with the soup
    html_game_list = soup.find('div', id='Top25') \
        .find_all('a', class_='topclick-list-element')
    game_list = []
    for i, game in enumerate(html_game_list):
        # Create list game item
        game = ListGame(
            id=i,
            name=html_game_list[i].find('div', class_='topclick-list-element-game-title').text.strip(),
            merchant=html_game_list[i].find('div', class_='topclick-list-element-game-merchant').text.strip(),
            price=html_game_list[i].find('span', class_='topclick-list-element-price').text.strip(),
            href=html_game_list[i]['href']
        )
        # Add it to the list
        game_list.append(game)

    return game_list


def get_game_from_url(game_url):
    # Get the game page
    html_text = requests.get(game_url).text
    # Create the soup
    soup = BeautifulSoup(html_text, 'lxml')

    # Get the game info
    game_info = soup.find_all('div', class_='game-info-table-value')

    game_release_date = game_info[0].text.strip()
    game_official_website = game_info[1].find('a')['href']
    game_developer = game_info[2].text.strip()
    game_publisher = game_info[3].text.strip()
    game_pegi = game_info[5].text.strip()
    game_description = soup.find('div', id='about') \
        .find('p').text.strip()

    # Need to perform some operations in some fields
    game_platforms = game_info[4].text.split('\n')
    game_platforms = split_platforms(game_platforms)
    game_platforms = list_to_str('/', game_platforms)

    game_tags = game_info[6].text.split('\n')
    game_tags = split_tags(game_tags)
    game_tags = list_to_str('/', game_tags)

    game_image_html = soup.find('img', class_='gamepage__image--first gallery-element-image')
    game_name = game_image_html.get('alt')
    game_image = game_image_html.get('src')

    # And save it to an object
    game = Game(
        name=game_name,
        release_date=game_release_date,
        official_website=game_official_website,
        developer=game_developer,
        publisher=game_publisher,
        platforms=game_platforms,
        pegi=game_pegi,
        tags=game_tags,
        description=game_description,
        image_url=game_image,
        page_url=game_url
    )

    return game


def search_game(game_name, page=None):
    game_name_formatted = list_to_str('+', game_name.split('-'))

    if page:
        html_text = requests.get(REQUEST_URL_SEARCH + game_name_formatted + f'/page-{page}').text
    else:
        html_text = requests.get(REQUEST_URL_SEARCH + game_name_formatted).text

    soup = BeautifulSoup(html_text, 'lxml')

    is_there_previous = False
    is_there_next = False

    # Mess with the soup
    html_game_list = soup.find_all('a', class_='search-results-row-link')
    game_list = []

    if len(html_game_list) > 0:
        for i, game in enumerate(html_game_list):
            if html_game_list[i].get('href'):
                # Create list game item
                game = ListGame(
                    id=i,
                    name=html_game_list[i].find('h2', class_='search-results-row-game-title').text.strip(),
                    info=html_game_list[i].find('div', class_='search-results-row-game-infos').text.strip(),
                    merchant=None,
                    price=html_game_list[i].find('div', class_='search-results-row-price').text.strip(),
                    href=html_game_list[i]['href']
                )
                # Add it to the list
                game_list.append(game)

        pagination = soup.find_all('li', class_='pagination-page')

        if len(pagination) > 0:
            active_page = soup.find('li', class_='pagination-page active').text.strip()

            if int(active_page) > 1:
                is_there_previous = True

            if pagination[-1].text.strip() != active_page:
                is_there_next = True

    return [is_there_previous, is_there_next, game_list]
