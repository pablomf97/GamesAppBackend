# gamesapp/serializers
from rest_framework import serializers
from .models import Game, ListGame, User


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['name', 'description', 'release_date', 'official_website',
                  'developer', 'publisher', 'platforms', 'pegi',
                  'tags', 'image_url', 'page_url']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['user', 'games']


class ListGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ListGame
        fields = ['name', 'info', 'merchant', 'price', 'href']
