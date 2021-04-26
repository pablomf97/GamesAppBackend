from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from GamesAPI.pagination import ResultSetPagination

from .ws import webscrapper

from .models import Game
from .serializers import GameSerializer, ListGameSerializer, OfferSerializer


# Create your views here.
class GameListView(ListAPIView):
    pagination_class = ResultSetPagination
    queryset = Game.objects.all().order_by('name')
    serializer_class = GameSerializer


class TopGamesView(APIView):

    # GET request - Retrieves the top 25 games
    def get(self, request):
        top_25_games = webscrapper.get_top_25()
        serialized_games = ListGameSerializer(top_25_games, many=True)
        return Response(serialized_games.data)


class GameView(APIView):

    # GET request - Retrieves the requested game
    def get(self, request):
        game_data = request.data

        if game_data.get('game_href'):
            game_url = game_data.get('game_href')
            if not game_url.startswith(webscrapper.REQUEST_URL_BASE):
                return Response({"error": "Oops! The game you requested doesn't exist..."},
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type="application/json")

            try:
                data = webscrapper.get_game_from_url(game_url)
                game = data.get('game')
                offers = data.get('offers')

                if Game.objects.filter(page_url=game.page_url).count() == 0:
                    game.save()

                return Response({
                    'game': GameSerializer(game).data,
                    'offers': OfferSerializer(offers, many=True).data
                })
            except Exception as ecxp:
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


class SearchView(APIView):

    # GET Request - Gets the list of games given a game name
    def get(self, request, game_name, page_number=None):

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
