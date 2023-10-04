import time
import tweepy
import requests
import bard


def get_news():
  """Gets the latest financial news from Bard."""
  news = bard.get_news(category="business", sources=["stockmarket", "finance"])
  return news

def generate_tweet(news):
  """Generates a tweet about the news."""
  headline = news["headline"]
  summary = news["summary"]
  hashtags = []
  for ticker in news["tickers"]:
    hashtags.append(ticker)
  hashtags.extend(["finance", "business", "stockmarket"])
  tweet = f"{summary} {hashtags[:2]}"
  return tweet

def post_tweet(tweet):
  """Posts a tweet to Twitter."""
  auth = tweepy.OAuthHandler("add token here", " add token here")
  auth.set_access_token("token", "token item")

  api = tweepy.API(auth)

  # Check if the tweet has already been posted
  tweets = api.user_timeline(count=10)
  for t in tweets:
    if t.text == tweet:
      return

  # Check if the tweet fits in 280 characters
  if len(tweet) > 280:
    tweet = tweet[:280]

  # Check if the tweet is new
  created_at = t.created_at
  now = time.time()
  if (now - created_at).seconds / 3600 < 1:
    return

  api.update_status(tweet)

def main():
  while True:
    news = get_news()

    # Check if there is any new news
    if news == []:
      time.sleep(3600)  # 1 hour
      continue

    tweet = generate_tweet(news)
    post_tweet(tweet)

    time.sleep(3600)  # 1 hour

if __name__ == "__main__":
  main()
