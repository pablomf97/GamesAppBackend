# news/urls.py
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import NewsView

urlpatterns = [
    # News URL patterns
    path('news/', NewsView.as_view(), name='latest_news'),
    path('news/<str:type_>', NewsView.as_view(), name='latest_news'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
