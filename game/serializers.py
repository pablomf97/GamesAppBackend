# game/serializers
from rest_framework import serializers
from .models import Game, ListGame


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['name', 'description', 'release_date', 'official_website',
                  'developer', 'publisher', 'platforms', 'pegi',
                  'tags', 'image_url', 'page_url']


class ListGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListGame
        fields = ['name', 'info', 'merchant', 'price', 'href']
