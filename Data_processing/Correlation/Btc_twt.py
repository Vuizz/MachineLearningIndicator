import os
import tweepy
import yfinance as yf
import pandas as pd
from textblob import TextBlob
from datetime import datetime, timedelta

# Set your Twitter API credentials
consumer_key = '<YOUR_CONSUMER_KEY>'
consumer_secret = '<YOUR_CONSUMER_SECRET>'
access_token = '<YOUR_ACCESS_TOKEN>'
access_token_secret = '<YOUR_ACCESS_TOKEN_SECRET>'

# Authenticate to the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Define a function to fetch tweets and perform sentiment analysis
def get_twitter_sentiment(keyword, start_date, end_date, num_tweets=1000):
    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang='en', since=start_date, until=end_date).items(num_tweets)
    
    sentiment_scores = []
    for tweet in tweets:
        sentiment = TextBlob(tweet.text).sentiment.polarity
        sentiment_scores.append(sentiment)
    
    return pd.Series(sentiment_scores).mean()

# Define the date range for the analysis
start_date = '2020-01-01'
end_date = '2021-09-30'

# Download historical data for Bitcoin
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Calculate daily average sentiment scores for tweets mentioning Bitcoin
sentiment_data = []
current_date = datetime.strptime(start_date, '%Y-%m-%d')
while current_date < datetime.strptime(end_date, '%Y-%m-%d'):
    next_date = current_date + timedelta(days=1)
    sentiment = get_twitter_sentiment('Bitcoin', current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
    sentiment_data.append({'Date': current_date, 'Sentiment': sentiment})
    current_date = next_date

sentiment_df = pd.DataFrame(sentiment_data).set_index('Date')

# Calculate daily returns for Bitcoin price and sentiment data
btc_returns = btc['Close'].pct_change().dropna()
sentiment_returns = sentiment_df.pct_change().dropna()

# Merge the two return series into a single DataFrame
combined_returns = pd.concat([btc_returns, sentiment_returns], axis=1).dropna()
combined_returns.columns = ['BTC', 'Sentiment']

# Calculate the correlation between Bitcoin and Twitter sentiment
correlation = combined_returns.corr()
print(correlation)
