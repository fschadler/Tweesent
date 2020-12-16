from django.shortcuts import render
from App_TwitterDataCollector.views import TwitterClient
from App_TwitterDataframe.views import TweetToDataframe
from App_ChartCreator.views import pie_chart_gen, hashtag_cloud_gen, word_cloud_gen, boxplot_gen, distribution_gen
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


"""
Class to create variables and dataframes which are rendered on the output page. 
"""

def analysis(request):
    """
    Importing App_TwitterDataFrame
    """
    twitter_client = TwitterClient()
    tweet_df = TweetToDataframe()
    tweets = twitter_client.get_tweets(request)
    df = tweet_df.tweets_to_data_frame(tweets)

    # Importing analyzer from vaderSentiment
    analyzer = SentimentIntensityAnalyzer()

    # Creates Dataframe Excel File
    df.to_excel("static/raw_tweets.xlsx")

    """
    Adding the sentiment Score to the Dataframe based on cleaned and translated Tweets
    """
    df['sentiment'] = [analyzer.polarity_scores(x)['compound'] for x in df['cleaned_english_tweets']]
    df['sentiment'] = np.round(df['sentiment'], decimals=2)

    """
    Dataframes for HTML: 
    """
    # Creates a slimmer Dataframe Table for the Output Page
    df_short = df[["html_ready_tweets", "sentiment"]]
    df_short_html = df_short.to_html(classes="table table-borderless table-hover table-striped", border=0,
                                     justify="left")

    # Dataframe which shows the top 5 Tweeters within the pulled data, based on highest follower count.
    df_top = df[["user_screen_name", "follower_count"]].nlargest(5, "follower_count")
    df_top = (df_top.rename(columns={'user_screen_name': 'Username', 'follower_count': 'Follower Count'}))
    df_top_html = df_top.to_html(classes="table table-borderless table-hover table-striped", index=False, border=0,
                                 justify="left")

    """
    Variables for HTML:
    """
    # Variable to display the average sentiment score.
    sentiment_average = round(sum(df["sentiment"]) / len(df["sentiment"]), 1)
    # Variable to display how many Tweets the user has requested.
    input_num_terms = len(df["tweets"])
    # Variable to display which search term the user has requested.
    input_hashtag = request.POST['input_hashtag']
    # Variable to display what time range the Tweets are based of.
    tweet_duration = max(df["date"]) - min(df["date"])
    # Variables to display amount of positive / neutral / negative Tweets
    count_positive = int(np.sum(df['sentiment'] > 0))
    count_neutral = int(np.sum(df['sentiment'] == 0))
    count_negative = int(np.sum(df['sentiment'] < 0))
    # Descriptive Statistics
    min_sentiment = df["sentiment"].min
    max_sentiment = df["sentiment"].max

    # Categorizes Sentiment Score into Negative, Positive and neutral
    if sentiment_average <= -0.05:
        sentiment_describe = "negative"
    elif sentiment_average > 0.05:
        sentiment_describe = "positive"
    else:
        sentiment_describe = "neutral"

    """
    Importing App_ChartCreator
    """
    word_cloud = word_cloud_gen(df)
    hashtag_cloud = hashtag_cloud_gen(df)
    chart = pie_chart_gen(count_positive, count_neutral, count_negative)
    boxplot = boxplot_gen(df)
    distribution = distribution_gen(df)

    # renders variables to analysis page
    if request.method == 'POST':
        return render(request, 'analysis.html', {'df_short_html': df_short_html, "sentiment_average": sentiment_average,
                                                   "input_num_terms": input_num_terms, "input_hashtag": input_hashtag,
                                                   "tweet_duration": tweet_duration, "df_top_html": df_top_html,
                                                   "count_positive": count_positive, "count_neutral": count_neutral,
                                                   "count_negative": count_negative, "min_sentiment": min_sentiment,
                                                   "max_sentiment": max_sentiment, "word_cloud": word_cloud,
                                                   "hashtag_cloud": hashtag_cloud,"chart": chart, "boxplot": boxplot,
                                                   "distribution": distribution,"sentiment_describe": sentiment_describe})


def contact(request):
    # renders contact page
    return render(request, 'Contact.html', {})


def faq(request):
    # renders faq page
    return render(request, 'FAQ.html', {})
