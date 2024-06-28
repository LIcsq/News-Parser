from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    """
    Serializer for News model.
    """
    class Meta:
        model = News
        fields = ['title', 'link', 'published', 'sentiment_score', 'trend_names']
