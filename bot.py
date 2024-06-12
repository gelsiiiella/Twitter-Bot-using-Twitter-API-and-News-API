from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv
import datetime
import requests
import json
import schedule
import time
import os


load_dotenv()

# News API credentials
news_api_key = os.getenv('NEWS_API_KEY')
# Twitter API credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')


def fetch_cybersecurity_news():
    url = f"https://newsapi.org/v2/everything?q=cybersecurity&apiKey={news_api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch news: {response.status_code}")
    news_data = response.json()
    articles = news_data.get('articles', [])
    return articles

def count_news(articles):
    total_articles = len(articles)
    return total_articles

# Post tweet
def post_tweet(text):
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret,
                          resource_owner_key=access_token, resource_owner_secret=access_token_secret)
    payload = {"text": text}
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
    if response.status_code != 201:
        raise Exception(f"Failed to post tweet: {response.status_code} {response.text}")
    print(f"Tweet posted successfully: {response.status_code}")


# Main function
def main():
    articles = fetch_cybersecurity_news()
    if not articles:
        print("No cybersecurity news found.")
        return

    # Analyze news
    total_articles = count_news(articles)
    print(f"Total cybersecurity articles analyzed: {total_articles}")

    # Generate and post tweets
    for article in articles[:5]:  # Tweet the top 5 articles
        title = article.get("title")
        url = article.get("url")
        tweet_text = f"{title} {url}"
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."
        try:
            post_tweet(tweet_text)
        except Exception as e:
            print(f"Error posting tweet: {e}")


if __name__ == "__main__":
    main()
    schedule.every().day.at("10:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)