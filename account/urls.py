# account/url.py
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterUserView, DeleteTokenView

urlpatterns = [
    # User URL patterns
    path('user/register/', RegisterUserView.as_view(), name='register'),
    path('user/login/', obtain_auth_token, name='login'),
    path('user/logout/', DeleteTokenView.as_view(), name='delete_token')
]

urlpatterns = format_suffix_patterns(urlpatterns)
