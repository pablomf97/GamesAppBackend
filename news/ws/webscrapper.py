from bs4 import BeautifulSoup
import requests

from enum import Enum

from news.models import Article

REQUEST_URL_BASE = 'https://www.allkeyshop.com/blog/category/allkeyshop-video-gaming-news/'


news_type = {
    'deals': 'deal-of-the-day-allkeyshop-news',
    'rewards': 'rewards-program',
    'giveaway': 'giveaway-allkeyshop-news',
    'gaming': 'gaming-news',
    'charity': 'charity',
    'top': 'games-like-top-10'
}


def get_news(type_=None):
    if type_:
        url = REQUEST_URL_BASE + news_type.get(type_)
    else:
        url = REQUEST_URL_BASE

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    return __get_articles_from_soup(soup)


def __get_articles_from_soup(soup):
    html_articles = soup.find_all('li', class_='article')
    articles = []

    if html_articles and len(html_articles) > 0:

        for article in html_articles:
            try:
                picture = article.find('img').get('src')
                headline = article.find(
                    'h2', class_='article-content-headline').text.strip()
                category = article.find(
                    'span', class_='article-content-digest-category').text.split('|')[0].strip()
                content_preview = article.find(
                    'p', class_='article-content-digest').text.split('\n')[2].strip()
                link = article.find('a').get('href')

                articles.append(Article(
                    picture=picture,
                    headline=headline,
                    category=category,
                    content_preview=content_preview,
                    link=link
                ))
            except:
                pass

    return articles
