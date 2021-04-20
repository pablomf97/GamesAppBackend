# account/url.py
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from .views import RegisterUserView, DeleteTokenView

urlpatterns = [
    # User URL patterns
    path('user/register/', RegisterUserView.as_view(), name='register'),
    path('user/login/', views.obtain_auth_token, name='generate_token'),
    path('user/logout/', DeleteTokenView.as_view(), name='delete_token')
]

urlpatterns = format_suffix_patterns(urlpatterns)
