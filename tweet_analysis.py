# UPDATE: THIS CODE HAS BEEN UPDATED TO LOGIN
# USERS MUST CREATE TWITTER DEVELOPER ACCOUNT @ https://developer.x.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

# INSTALL TWEEPY + DOTENV FOR TWITTER ACCESS

import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# REPLACE W YOUR CREDENTIALS
api_key = 'INPUT_HERE'
api_secret = 'INPUT_HERE'
access_token = 'INPUT_HERE'
access_token_secret = 'INPUT_HERE'

credentials = tweepy.OAuth1UserHandler(
    api_key, api_secret, access_token, access_token_secret)
api = tweepy.api(credentials)

ticker = input('WHAT STOCK DO YOU WANT TO ANALYZE?')  # ASSUME VALID INPUT
search = '$' + ticker

vader = SentimentIntensityAnalyzer()
compound_scores = []

# GET TWEETS
tweets = api.search_tweets(q=search, count=10)

for tweet in tweets:
    tweet_info = tweet.text
    tweet_sentiment = vader.polarity_scores(tweet_info)
    compound_score = tweet_sentiment['compound']
    compound_scores.append(compound_score)


avg_score = sum(compound_scores) / len(compound_scores)

if avg_score > 0:
    label = 'Positive'
elif avg_score < 0:
    label = 'Negative'
else:
    label = 'Neutral'

print(ticker + ' IS ' + label + ' AND HAS AN AVG SCORE OF ' + str(avg_score))
