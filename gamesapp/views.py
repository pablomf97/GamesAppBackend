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
        data = request.data
        try:
            game_url = data['href']

            return Response({"Test": "test"})

        except KeyError:
            game_name = data['game_name']

            return Response({"Test2": "test2"})
