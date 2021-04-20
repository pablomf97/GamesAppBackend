# games/urls.py
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import GameView, GameListView, SearchView, TopGamesView

urlpatterns = [
    # Game URL patterns
    path('games/all', GameListView.as_view()),
    path('games/top-25', TopGamesView.as_view()),
    path('games/game', GameView.as_view()),
    path('games/search/<str:game_name>', SearchView.as_view()),
    path('games/search/<game_name>/<page_number>', SearchView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
