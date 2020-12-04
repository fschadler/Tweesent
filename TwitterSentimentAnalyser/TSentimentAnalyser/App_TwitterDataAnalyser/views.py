from django.shortcuts import render
from App_TwitterDataCollector.views import TwitterClient
from App_TwitterDataframe.views import TweetToDataframe
import numpy as np
from textblob import TextBlob


"""
This app is used to analyse the Dataframe from App_TwitterDataframe.
"""


class TweetSentiment:
    """
    Analyses the sentiment score of the cleaned tweets.
    """
    clean_tweet = TweetToDataframe.clean_tweet

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        return analysis.sentiment.polarity


"""
Class to create variables and dataframes which are rendered on the output page. 
"""


def prediction(request):

    twitter_client = TwitterClient()
    tweet_df = TweetToDataframe()
    tweet_sentiment = TweetSentiment()
    clean_tweet = TweetToDataframe.clean_tweet
    tweets = twitter_client.get_tweets(request)
    df = tweet_df.tweets_to_data_frame(tweets)

    # Adds the sentiment Score to the Dataframe
    df['sentiment'] = np.array([tweet_sentiment.analyze_sentiment(tweet) for tweet in df['tweets']])

    # Do we still need those lists? @Florin
    list_of_tweets = list(df["tweets"])
    list_of_cleaned_tweets = list(df["cleaned_tweets"])
    list_of_english_tweets = list(df["english_tweets"])
    list_of_cleaned_english_tweets = list(df["cleaned_english_tweets"])

    """
    Dataframes for HTML: 
    """
    # Creates a slimmer Dataframe Table for the Output Page
    df_short = df[["tweets","sentiment"]]
    df_short_html = df_short.to_html
    # Dataframe which shows the top 5 Tweeters within the pulled data, based on highest follower count.
    df_top = df[["user_screen_name", "follower_count"]].nlargest(5, "follower_count")
    df_top_html = df_top.to_html(index=False, header=False)
    """
    Variables for HTML:
    """
    # Variable to display the average sentiment score.
    sentiment_average = round(sum(df["sentiment"]) / len(df["sentiment"]), 1)
    # Variable to display how many Tweets the user has requested.
    input_num_terms = (request.POST['num_terms'])
    # Variable to display which search term the user has requested.
    input_hashtag = request.POST['hashtag']
    # Variable to display what time range the Tweets are based of.
    tweet_duration = max(df["date"]) - min(df["date"])
    # Variables to display amount of positive / neutral / negative Tweets
    count_positive = int(np.sum(df['sentiment'] > 0))
    count_neutral = int(np.sum(df['sentiment'] == 0))
    count_negative = int(np.sum(df['sentiment'] < 0))


    if request.method == 'POST':
        return render(request, 'prediction.html', {'df_short_html': df_short_html, "sentiment_average": sentiment_average,
                                                   "input_num_terms": input_num_terms, "input_hashtag": input_hashtag,
                                                   "tweet_duration": tweet_duration, "df_top_html": df_top_html,
                                                   "clean_tweet": clean_tweet, "count_positive": count_positive,
                                                   "count_neutral": count_neutral, "count_negative": count_negative,
                                                   "clean_tweet": clean_tweet})


def contact(request):
    return render(request, 'contact.html', {})


def home(request):
    return render(request, 'home', {})
