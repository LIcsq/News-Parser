from rest_framework import generics
from .models import News
from .serializers import NewsSerializer

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
