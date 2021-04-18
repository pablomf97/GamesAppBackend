# gamesapp/serializers
from rest_framework import serializers
from .models import Game, ListGame


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['name', 'release_date', 'official_website',
                  'developer', 'publisher', 'platforms', 'pegi',
                  'tags', 'image_url', 'page_url']


class ListGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ListGame
        fields = ['name', 'merchant', 'price', 'href']
