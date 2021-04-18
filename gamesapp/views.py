from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .ws import webscrapper

from .models import Game
from .serializers import GameSerializer, ListGameSerializer


# Create your views here.
class GameListView(APIView):
    # GET request - Retrieves every game on the db
    def get(self, request):
        games = Game.objects.all()
        serialized_games = GameSerializer(games, many=True)
        return Response(serialized_games.data)


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

            # Check if the game exist in the database
            try:
                game_db = Game.objects.get(page_url=game_url)
                return Response(GameSerializer(game_db).data)
            except ObjectDoesNotExist:
                game = webscrapper.get_game_from_url(game_url)
                game.save()
                return Response(GameSerializer(game).data)

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
