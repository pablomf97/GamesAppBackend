"""
This class manages everything related
to gaming news, which is, in this case:
    - NewsView --> Only accepts GET request and returns
    the latest news within a category (if it was provided),
    or just the latest news in general.
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .ws import webscrapper as ws

from .serializers import ArticleSerializer


class NewsView(APIView):
    """
    Manages requests to news/
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, type_=None):
        """
        GET request - Returns the latests news depending on the type specified
        """

        # If the type was was specified...
        if type_ and type_ in ws.news_type:
            # ...we get the news that fit in that type or category.
            articles = ws.get_news(type_)
        else:
            # Otherwise, we just get the latest news.
            articles = ws.get_news()

        # We serialize them and return them as JSON.
        serialized_articles = ArticleSerializer(articles, many=True)
        return Response(serialized_articles.data)
