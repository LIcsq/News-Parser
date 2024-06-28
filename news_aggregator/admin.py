from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    """Admin view for News model."""
    list_display = ('title', 'link', 'published', 'sentiment_score', 'trend_names')

admin.site.register(News, NewsAdmin)
