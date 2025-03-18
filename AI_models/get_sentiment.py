import requests
import time

API_KEY = "cf96f0e06e204e16885d2256742722a9"
NEWS_API_URL = "https://newsapi.org/v2/everything?q={}&apiKey={}"

def get_news_sentiment(query, max_retries=3, wait_time=10):
    """Fetch sentiment data from news API and handle errors properly."""
    
    for attempt in range(max_retries):
        response = requests.get(NEWS_API_URL.format(query, API_KEY))
        data = response.json()

        if response.status_code == 429:
            print(f"Rate limit reached. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            continue  # Retry the request

        if "articles" not in data:
            print("API response does not contain 'articles'. Possible rate limit or API issue.")
            return []  # Return an empty list instead of crashing

        return [article["title"] for article in data["articles"][:10]]  # Return first 10 article titles

    print("Max retries reached. Could not fetch news data.")
    return []
