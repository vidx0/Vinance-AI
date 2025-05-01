import requests
import time
import numpy as np

API_KEY = "key"  # Replace with your actual API key
NEWS_API_URL = "https://newsapi.org/v2/everything?q={}&apiKey={}"

from textblob import TextBlob

def get_news_sentiment(query, max_retries=3, wait_time=10):
    """Fetch sentiment data from news API and return an average sentiment score."""
    for attempt in range(max_retries):
        response = requests.get(NEWS_API_URL.format(query, API_KEY))
        data = response.json()

        if response.status_code == 429:
            print(f"Rate limit reached. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            continue  # Retry the request

        if "articles" not in data:
            print("API response does not contain 'articles'. Possible rate limit or API issue.")
            return 0.0  # Default to neutral sentiment

        headlines = [article["title"] for article in data["articles"][:10]]
        sentiment_scores = [TextBlob(title).sentiment.polarity for title in headlines]
        
        return np.mean(sentiment_scores) if sentiment_scores else 0.0

    print("Max retries reached. Could not fetch news data.")
    return 0.0
