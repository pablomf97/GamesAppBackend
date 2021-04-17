from bs4 import BeautifulSoup
import requests

from gamesapp.models import ListGame
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
