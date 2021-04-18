from bs4 import BeautifulSoup
import requests

from gamesapp.models import ListGame, Game

from ..utils.utils import *


REQUEST_URL_BASE = 'https://www.allkeyshop.com/blog/'


def get_top_25():
    # Get the top 25 games
    html_text = requests.get(REQUEST_URL_BASE).text
    # Create the soup
    soup = BeautifulSoup(html_text, 'lxml')

    # Mess with the soup
    html_game_list = soup.find('div', id='Top25')\
        .find_all('a', class_='topclick-list-element')
    game_list = []
    for i, game in enumerate(html_game_list):
        # Create list game item
        game = ListGame(
            i,
            html_game_list[i].find('div', class_='topclick-list-element-game-title').text.strip(),
            html_game_list[i].find('div', class_='topclick-list-element-game-merchant').text.strip(),
            html_game_list[i].find('span', class_='topclick-list-element-price').text.strip(),
            html_game_list[i]['href']
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
    game_description = soup.find('div', id='about')\
        .find('p').text.strip()

    # Need to perform some operations in some fields
    game_platforms = game_info[4].text.split('\n')
    game_platforms = split_platforms(game_platforms)
    game_platforms = list_to_str(game_platforms)

    game_tags = game_info[6].text.split('\n')
    game_tags = split_tags(game_tags)
    game_tags = list_to_str(game_tags)

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
