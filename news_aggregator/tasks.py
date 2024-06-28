from celery import shared_task
from .models import News
from .utils import fetch_rss_feed, fetch_google_trends, match_news_with_trends, enrich_with_sentiment
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_news():
    logger.info("Starting update_news task")
    rss_url = "https://tsn.ua/rss/full.rss"
    news_entries = fetch_rss_feed(rss_url)
    trends = fetch_google_trends(geo='united_states')
    matched_news = match_news_with_trends(news_entries, trends)
    enriched_news = enrich_with_sentiment(matched_news)

    for news in enriched_news:
        obj, created = News.objects.update_or_create(
            title=news['title'],
            defaults={
                'link': news['link'],
                'published': news['published'],
                'trend_names': news['trend'],
                'sentiment_score': news['sentiment_score']
            }
        )
        logger.info(f"News {'created' if created else 'updated'}: {obj.title}")

    logger.info("News update task completed successfully.")
