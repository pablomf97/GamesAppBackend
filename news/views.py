from rest_framework.views import APIView
from rest_framework.response import Response

from .ws import webscrapper as ws

from .serializers import ArticleSerializer


class NewsView(APIView):
    """
    Manages requests to news/
    """

    def get(self, request, type_=None):
        """
        GET request - Returns the latests news depending on the type specified
        """
        
        if type_ and type_ in ws.news_type:
            articles = ws.get_news(type_)
        else:
            articles = ws.get_news()

        serialized_articles = ArticleSerializer(articles, many=True)
        return Response(serialized_articles.data)
