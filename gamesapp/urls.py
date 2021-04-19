# gamesapp/urls.py
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from gamesapp.views import game_views, user_views

urlpatterns = [
    # Game URL patterns
    path('games/all', game_views.GameListView.as_view()),
    path('games/top-25', game_views.TopGamesView.as_view()),
    path('games/game', game_views.GameView.as_view()),
    path('games/search/<str:game_name>', game_views.SearchView.as_view()),
    path('games/search/<game_name>/<page_number>', game_views.SearchView.as_view()),

    # User URL patterns
    path('user/register/', user_views.RegisterUserView.as_view()),
    path('user/login/', views.obtain_auth_token),
    path('user/logout/', user_views.DeleteTokenView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
