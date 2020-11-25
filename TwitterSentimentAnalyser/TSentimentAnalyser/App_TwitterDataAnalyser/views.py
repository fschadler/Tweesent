from django.shortcuts import render
from TwitterSentimentAnalyser.TSentimentAnalyser.App_TwitterDataCollector.views import TwitterClient
import re
import numpy as np
import pandas as pd
from textblob import TextBlob
from googletrans import Translator



"""
This app is used to clean and analyse the pulled Tweets from the App_TwitterDataCollector and appends them in a pandas.series. 
"""

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, "", input_txt)
    return input_txt

def clean_tweets(lst):
    # remove twitter Return handles (RT @xxx:)
    lst = np.vectorize(remove_pattern)(lst, "RT @[\w]*:")
    # remove twitter handles (@xxx)
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    # remove special characters, numbers, punctuations (except for #)
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    return lst


class TweetAnalyser:
    """
    Used for cleaning, analyzing and appending the tweets in a pandas dataframe.
    """
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        return analysis.sentiment.polarity

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        translator = Translator()

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['lang'] = np.array([tweet.lang for tweet in tweets])
        df['user_id'] = np.array([tweet.user.id for tweet in tweets])
        df['user_screen_name'] = np.array([tweet.user.screen_name for tweet in tweets])
        df['follower_count'] = np.array([tweet.user.followers_count for tweet in tweets])
        df["english_tweets"] = df["tweets"].apply(lambda x: translator.translate(x, dest="en").text)
        df["english_tweets"] = df["english_tweets"].astype("str")
        df["cleaned_tweets"] = df["tweets"].map(lambda x: clean_tweets(x))
        df["cleaned_english_tweets"] = df["english_tweets"].map(lambda x: clean_tweets(x))
        return df


"""
Displays Dataframe Table 
"""


def prediction(request):

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyser()
    # Tweets filtered based on manual user input
    tweets = twitter_client.get_tweets(request)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    list_of_tweets = list(df["tweets"])
    list_of_cleaned_tweets = list(df["cleaned_tweets"])
    list_of_english_tweets = list(df["english_tweets"])
    list_of_cleaned_english_tweets = list(df["cleaned_english_tweets"])
    df_html = df.to_html
    sentiment_average = {}
    sentiment_average = sum(df["sentiment"]) / len(df["sentiment"])
    if request.method == 'POST':
        return render(request, 'prediction.html', {'html_table': df_html, "sentiment_average": sentiment_average})



