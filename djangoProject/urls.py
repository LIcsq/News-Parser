from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the News Aggregator!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('news_aggregator.urls')),
    path('', home),  # Добавление корневого URL
]
