from django.urls import path
from news_aggregator.views import NewsListView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news-list'),
]
