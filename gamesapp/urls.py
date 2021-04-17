# gamesapp/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from gamesapp import views

urlpatterns = [
    path('games/all', views.GameListView.as_view()),
    path('games/top-25', views.TopGamesView.as_view()),
    path('games/game', views.GameView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
