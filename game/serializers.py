# game/serializers
from rest_framework import serializers
from .models import Game, ListGame, Offer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'user_rating', 'media_rating',
                  'release_date', 'official_website',
                  'developer', 'publisher', 'platforms', 'pegi',
                  'tags', 'image_url', 'page_url']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['shop', 'region', 'platform', 'edition',
                  'price_before_fees', 'shop_url']


class ListGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListGame
        fields = ['name', 'info', 'merchant', 'price', 'href']
