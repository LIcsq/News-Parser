import feedparser
from pytrends.request import TrendReq
import re
import logging
from translate import Translator
from datetime import datetime
import subprocess
import json
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
translator = Translator(to_lang="uk")

# Function to fetch data from an RSS feed
def fetch_rss_feed(url: str) -> List[Dict[str, Any]]:
    """
    Fetches RSS feed data from the given URL.

    Args:
        url (str): The URL of the RSS feed.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the title, link, and published date of each entry.
    """
    logger.info(f"Fetching RSS feed from {url}")
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        # Convert the published date to a standard format
        published = entry.published
        try:
            published_datetime = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %z')
            published_str = published_datetime.strftime('%Y-%m-%d %H:%M:%S%z')
        except ValueError as e:
            logger.error(f"Error parsing date {published}: {e}")
            published_str = None
        entries.append({
            'title': entry.title,
            'link': entry.link,
            'published': published_str
        })
        logger.debug(f"Fetched news: {entry.title}")
    return entries

# Function to fetch Google Trends for a given region
def fetch_google_trends(geo: str = 'united_states') -> List[str]:
    """
    Fetches current Google Trends for the specified region and translates them to Ukrainian.

    Args:
        geo (str): The region for which to fetch trends. Defaults to 'united_states'.

    Returns:
        List[str]: A list of translated trends.
    """
    logger.info(f"Fetching Google trends for {geo}")
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_searches_df = pytrends.trending_searches(pn=geo)
    trends = trending_searches_df[0].tolist()
    logger.debug(f"Fetched trends: {trends}")

    # Translate trends to Ukrainian
    translated_trends = []
    for trend in trends:
        translated = translator.translate(trend)
        translated_trends.append(translated)
        logger.debug(f"Translated trend: {trend} -> {translated}")

    return translated_trends

# Function to normalize text
def normalize_text(text: str) -> str:
    """
    Normalizes the text by removing non-alphanumeric characters and converting to lowercase.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The normalized text.
    """
    normalized_text = re.sub(r'\W+', ' ', text).lower()
    logger.debug(f"Normalized text: {normalized_text}")
    return normalized_text

# Function to match news entries with trends
def match_news_with_trends(news_entries: List[Dict[str, Any]], trends: List[str]) -> List[Dict[str, Any]]:
    """
    Matches news entries with Google Trends based on normalized text.

    Args:
        news_entries (List[Dict[str, Any]]): List of news entries.
        trends (List[str]): List of trends.

    Returns:
        List[Dict[str, Any]]: A list of matched news entries with trend information.
    """
    logger.info("Matching news with trends")
    matched_news = []
    trends_normalized = set(normalize_text(trend) for trend in trends)

    for entry in news_entries:
        title_normalized = normalize_text(entry['title'])
        logger.debug(f"Processing news title: {title_normalized}")

        # Check for intersection of words in the title with trends
        if trends_normalized & set(title_normalized.split()):
            matched_news.append({
                'title': entry['title'],
                'link': entry['link'],
                'published': entry['published'],
                'trend': ', '.join(trend for trend in trends if normalize_text(trend) in title_normalized)
            })
            logger.info(f"News matched: {entry['title']}")

    logger.info(f"Matched {len(matched_news)} news items with trends")
    return matched_news

# Function to get sentiment score using OpenAI API
def get_sentiment_score(text: str) -> float:
    """
    Gets sentiment score for the given text using OpenAI API.

    Args:
        text (str): The text for sentiment analysis.

    Returns:
        float: The sentiment score ranging from -1 (very negative) to 1 (very positive).
    """
    logger.debug(f"Getting sentiment score for text: {text}")

    command = [
        'curl',
        '-X', 'POST',
        'https://api.openai.com/v1/chat/completions',
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer sk-py-hr-J4a4k4nfgSxKDO9H5UZ8T3BlbkFJn14ecbJLvu4VZhnY3Xtv',
        '-d', json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system",
                 "content": "You are an assistant providing sentiment analysis. Please rate the sentiment of the following text from -1 (very negative) to 1 (very positive)."},
                {"role": "user", "content": text}
            ],
            "max_tokens": 50,
            "n": 1,
            "stop": None,
            "temperature": 0.0
        })
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(f"Error calling OpenAI API: {result.stderr}")
        raise Exception(f"Error calling OpenAI API: {result.stderr}")

    logger.debug(f"Full response from OpenAI API: {result.stdout}")

    try:
        response = json.loads(result.stdout)
        sentiment = response['choices'][0]['message']['content'].strip()
        logger.info(f"Sentiment score for text '{text}' is {sentiment}")

        sentiment_value = re.search(r'(-?\d+(\.\d+)?)', sentiment)
        if sentiment_value:
            return float(sentiment_value.group(0))

        if "very positive" in sentiment or "positive" in sentiment:
            return 1.0
        elif "very negative" in sentiment or "negative" in sentiment:
            return -1.0
        else:
            return 0.0
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON response: {e}")
        raise Exception(f"Error parsing JSON response: {e}")
    except KeyError as e:
        logger.error(f"Missing key in response: {e}")
        raise Exception(f"Missing key in response: {e}")
    except AttributeError as e:
        logger.error(f"Error extracting numeric value from sentiment: {e}")
        raise Exception(f"Error extracting numeric value from sentiment: {e}")

# Function to enrich matched news with sentiment scores
def enrich_with_sentiment(matched_news: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enriches the matched news entries with sentiment scores.

    Args:
        matched_news (List[Dict[str, Any]]): List of matched news entries.

    Returns:
        List[Dict[str, Any]]: A list of enriched news entries with sentiment scores.
    """
    logger.info("Enriching news with sentiment scores")
    for news in matched_news:
        news['sentiment_score'] = get_sentiment_score(news['title'])
    logger.info("Enrichment completed")
    return matched_news
