# account/url.py
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from .views import IsGameFavourited, RegisterUserView, DeleteTokenView, AddGameToAccount, GetAccountGames, RemoveGameFromAccount

urlpatterns = [
    # User URL patterns
    path('user/register/', RegisterUserView.as_view(), name='register'),
    path('user/login/', obtain_auth_token, name='login'),
    path('user/logout/', DeleteTokenView.as_view(), name='delete_token'),

    path('user/is-favourited/<game_id>/', IsGameFavourited.as_view(), name='is_favourited'),
    path('user/add-game/<game_id>/', AddGameToAccount.as_view(), name='add_game'),
    path('user/remove-game/<game_id>/', RemoveGameFromAccount.as_view(), name='remove_game'),
    path('user/get-games/', GetAccountGames.as_view(), name='get_games'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
