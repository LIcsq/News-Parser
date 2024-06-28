from django.db import models

class News(models.Model):
    """Model representing a news article."""
    title = models.CharField(max_length=255)
    link = models.URLField()
    published = models.DateTimeField()
    sentiment_score = models.FloatField()
    trend_names = models.TextField()

    def __str__(self):
        return self.title
