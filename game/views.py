from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from GamesAPI.pagination import ResultSetPagination

from .ws import webscrapper

from .models import Game
from .serializers import GameSerializer, ListGameSerializer, OfferSerializer


class GameListView(ListAPIView):
    """ 
    Manages requests to /games/all
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    pagination_class = ResultSetPagination
    queryset = Game.objects.all().order_by('name')
    serializer_class = GameSerializer


class TopGamesView(APIView):
    """ 
    Manages requests to /games/top-25
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        GET request - Retrieves the top 25 games
        """
        top_25_games = webscrapper.get_top_25()
        serialized_games = ListGameSerializer(top_25_games, many=True)
        return Response(serialized_games.data)


class GameView(APIView):
    """
    Manages the requests to /games/game
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    http_method_names = ['post']
    
    def post(self, request):
        """
        POST request - Retrieves the requested game
        """

        game_data = request.data

        if game_data.get('game_href'):
            game_url = game_data.get('game_href')
            if not game_url.startswith(webscrapper.REQUEST_URL_BASE):
                return Response({"error": "Oops! There was something wrong with the request..."},
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type="application/json")

            if Game.objects.filter(page_url=game_url).count() > 0:
                db_game = Game.objects.get(page_url=game_url)
                return Response(GameSerializer(db_game).data)

            try:
                game = webscrapper.get_game_from_url(game_url)

                if Game.objects.filter(page_url=game.page_url).count() == 0:
                    game.save()

                return Response(GameSerializer(game).data)
            except:
                return Response({"error": "There was an error while trying to perform the operation..."},
                                status=status.HTTP_404_NOT_FOUND,
                                content_type="application/json")

        elif game_data.get('game_name'):
            try:
                game_name = game_data.get('game_name')
                game_db = Game.objects.get(name=game_name)
                return Response(GameSerializer(game_db).data)
            except ObjectDoesNotExist:
                return Response({"error": "Oops! The game you requested doesn't exist..."},
                                status=status.HTTP_404_NOT_FOUND,
                                content_type="application/json")
        else:
            return Response({"error": "Oops! The game you requested doesn't exist..."},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")


class GameOffersView(APIView):
    """
    Returns the list of offers for a game
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    http_method_names = ['post']

    def post(self, request):
        """
        GET request - Gets the list of offers given
        either a game name or a game url
        """
        game_url = ""

        if request.data.get('game_url'):
            game_url = request.data.get('game_url')
        elif request.data.get('game_name'):
            try:
                game_name = request.data.get('game_name')
                game = Game.objects.get(name=game_name)
                game_url = game.page_url
            except:
                return Response(
                    {
                        "message": "Oops! Could not find the "
                        + "game you were looking for..."
                    },
                    status=status.HTTP_404_NOT_FOUND)

        if game_url:
            try:
                offers = webscrapper.get_game_offers(game_url)

                return Response(OfferSerializer(offers, many=True).data)
            except:
                return Response(
                    {
                        "message": "Oops! Something went wrong while "
                        + "trying to perform the operation"
                    }
                )

        return Response(
            {
                "message": "Oops! We could not understand your request..."
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class SearchView(APIView):
    """
    Returns the list of games that match the given name
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, game_name, page_number=None):
        """
        GET Request - Gets the list of games given a game name
        """

        if game_name:
            game_list = (webscrapper.search_game(game_name) if not page_number
                         else webscrapper.search_game(game_name, page_number))

            return Response({
                "search_results": ListGameSerializer(game_list[2], many=True).data,
                "is_there_next": game_list[1],
                "is_there_previous": game_list[0]
            })
        else:
            return Response({"error": "Oops! Sorry we didn't understand your request..."},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")
