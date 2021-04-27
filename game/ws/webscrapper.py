"""
This file contains the webscrapper
that will get the info related to games.
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from game.models import ListGame, Game, Offer

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
            name=html_game_list[i].find(
                'div', class_='topclick-list-element-game-title').text.strip(),
            merchant=html_game_list[i].find(
                'div', class_='topclick-list-element-game-merchant').text.strip(),
            price=html_game_list[i].find(
                'span', class_='topclick-list-element-price').text.strip(),
            href=html_game_list[i]['href']
        )
        # Add it to the list
        game_list.append(game)

    return game_list


def setup_selenium():
    """
    Creates a browser that will allow us 
    to get dynamic content from the website.
    """
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    return webdriver.Firefox(
        # UNCOMMENT WHEN IN LINUX executable_path="drivers/geckodriver-linux",
        executable_path="drivers/geckodriver-macos",
        firefox_options=options
    )


def get_game_from_url(game_url):
    # Get the page html
    html_text = requests.get(game_url).text
    # Create the soup
    soup = BeautifulSoup(html_text, 'lxml')

    # Start scrapping info
    return __get_game_details(
        soup=soup,
        game_url=game_url
    )


def get_game_offers(game_url):
    # Get the game page using selenium
    # because it has dynamic content
    driver = setup_selenium()
    driver.get(game_url)

    # Wait until the offers appear in the webpage
    WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_id('offer_offer'))

    # Create the soup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Start scrapping info
    return __get_game_offers(soup)


def __get_game_details(soup, game_url):
    # Get the game info
    game_info = soup.find_all('div', class_='game-info-table-value')

    try:
        game_release_date = game_info[0].text.strip()
    except:
        game_release_date = 'No info about the release date'

    try:
        game_official_website = game_info[1].find('a')['href']
    except:
        game_official_website = 'No info about the official website'

    try:
        game_developer = game_info[2].text.strip()
    except:
        game_developer = 'No info about the developer'

    try:
        game_publisher = game_info[3].text.strip()
    except:
        game_publisher = 'No info about the publisher'

    try:
        game_pegi = game_info[5].text.strip()
    except:
        game_pegi = 'No info about the age restriction'

    try:
        game_description = soup.find('div', id='About') \
            .find('p').text.strip()
    except AttributeError:
        try:
            game_description = soup.find('div', id='about') \
                .find('p').text.strip()
        except:
            game_description = 'No info about the game'
    except:
        game_description = 'No info about the game'

    # Need to perform some operations in some fields
    try:
        game_platforms = game_info[4].text.split('\n')
        game_platforms = split_platforms(game_platforms)
        game_platforms = list_to_str('/', game_platforms)
    except:
        game_platforms = 'No info about the platforms'

    try:
        game_tags = game_info[6].text.split('\n')
        game_tags = split_tags(game_tags)
        game_tags = list_to_str('/', game_tags)

        if '--' in game_tags:
            game_tags = 'No tags assigned for this game'
    except:
        game_tags = 'No info about the tags'

    try:
        game_image_html = soup.find(
            'img', class_='gamepage__image--first gallery-element-image')
        game_name = game_image_html.get('alt')
        game_image = game_image_html.get('src')
    except:
        game_name = 'No info about the name'
        game_image = 'No info about the image'

    try:
        game_user_rating = soup.find(
            'span', class_='hint').find('span').text.strip()
    except:
        game_user_rating = 'No info about the rating'

    try:
        game_media_rating = soup.find(
            'div',
            class_='metacritic-button metacritic-button-with-text metacritic-button-green'
        ).text.strip()
        game_media_rating = game_media_rating.split('\n')[-1].strip()
    except:
        game_media_rating = 'No info about the media rating'

    # And save it to an object
    return Game(
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
        page_url=game_url,
        user_rating=game_user_rating,
        media_rating=game_media_rating
    )


def __get_game_offers(soup):
    offers = []
    game_offers = soup.find_all('div', id='offer_offer')

    for i, item in enumerate(game_offers):
        if i != 0:
            try:
                offers.append(
                    Offer(
                        shop=item.find(
                            'span', class_='offers-merchant-name').text.strip(),
                        platform=item.find(
                            'div', id='offer_region_name').text.strip(),
                        edition=item.find(
                            'a', class_='d-inline-block').text.strip(),
                        price_before_fees=item.find(
                            'span', class_='x-offer-price').text.strip(),
                        shop_url=item.find(
                            'a', class_='d-none d-lg-block buy-btn x-offer-buy-btn').get('href')
                    )
                )
            except:
                pass

    return offers


def search_game(game_name, page=None):
    game_name_formatted = list_to_str('+', game_name.split('-'))

    if page:
        html_text = requests.get(
            REQUEST_URL_SEARCH + game_name_formatted + f'/page-{page}').text
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
                    name=html_game_list[i].find(
                        'h2', class_='search-results-row-game-title').text.strip(),
                    info=html_game_list[i].find(
                        'div', class_='search-results-row-game-infos').text.strip(),
                    merchant=None,
                    price=html_game_list[i].find(
                        'div', class_='search-results-row-price').text.strip(),
                    href=html_game_list[i]['href']
                )
                # Add it to the list
                game_list.append(game)

        pagination = soup.find_all('li', class_='pagination-page')

        if len(pagination) > 0:
            active_page = soup.find(
                'li', class_='pagination-page active').text.strip()

            if int(active_page) > 1:
                is_there_previous = True

            if pagination[-1].text.strip() != active_page:
                is_there_next = True

    return [is_there_previous, is_there_next, game_list]
