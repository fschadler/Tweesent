from django.shortcuts import render
from App_TwitterDataCollector.views import TwitterClient
from App_TwitterDataframe.views import TweetToDataframe
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS
from .utils import get_plot, get_wordcloud, get_hashtagcloud

"""
Class to create variables and dataframes which are rendered on the output page. 
"""
analyzer = SentimentIntensityAnalyzer()

def prediction(request):

    twitter_client = TwitterClient()
    tweet_df = TweetToDataframe()
    tweets = twitter_client.get_tweets(request)
    df = tweet_df.tweets_to_data_frame(tweets)

    # Adds the sentiment Score to the Dataframe based on cleaned and translated Tweets
#    df['sentiment'] = df['cleaned_english_tweets'].apply(lambda tweet: TextBlob(tweet).sentiment.polarity)
#    df['sentiment'] = np.round(df['sentiment'], decimals=2)
    df['sentiment'] = [analyzer.polarity_scores(x)['compound'] for x in df['cleaned_english_tweets']]
    df['sentiment'] = np.round(df['sentiment'], decimals=2)

    # Do we still need those lists? @Florin
    list_of_tweets = list(df["tweets"])
    list_of_cleaned_tweets = list(df["cleaned_tweets"])
    list_of_english_tweets = list(df["english_tweets"])
    list_of_cleaned_english_tweets = list(df["cleaned_english_tweets"])

    """
    Dataframes for HTML: 
    """
    # Creates a slimmer Dataframe Table for the Output Page
    df_short = df[["tweets", "sentiment"]]
    df_short_html = df_short.to_html(classes="table table-borderless table-hover table-striped", border=0, justify="left")

    # Dataframe which shows the top 5 Tweeters within the pulled data, based on highest follower count.
    df_top = df[["user_screen_name", "follower_count"]].nlargest(5, "follower_count")
    df_top = (df_top.rename(columns={'user_screen_name': 'Username', 'follower_count': 'Follower Count'}))
    df_top_html = df_top.to_html(classes="table table-borderless table-hover table-striped", index=False, border=0, justify="left")
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
    # Descriptive Statistics
    min_sentiment = df["sentiment"].min
    max_sentiment = df["sentiment"].max
    std_sentiment = round(df["sentiment"].std(), 2)

    """
    Pie Chart Generation
    """

    x = [count_positive,count_neutral,count_negative]
    chart = get_plot(x)

    """
    WordCloud Generation
    """
    stopwords = set(STOPWORDS)
    all_words = ' '.join([text for text in list_of_cleaned_english_tweets])
    y = WordCloud(background_color='white', stopwords=stopwords, width=1600, height=800, random_state=21,
                          colormap='jet', max_words=50, max_font_size=200).generate(all_words)

    hashtag_list_tweets = list(df["tweets"].str.findall(r"#(\w+)").sum())
    all_hashtags = ' '.join([hashtag for hashtag in hashtag_list_tweets])
    z = WordCloud(background_color='white', stopwords=stopwords, width=1600, height=800, random_state=21,
                          colormap='jet', max_words=50, max_font_size=200).generate(all_hashtags)

    word_cloud = get_wordcloud(y)


    hashtag_cloud = get_hashtagcloud(z)



    if request.method == 'POST':
        return render(request, 'prediction.html', {'df_short_html': df_short_html, "sentiment_average": sentiment_average,
                                                   "input_num_terms": input_num_terms, "input_hashtag": input_hashtag,
                                                   "tweet_duration": tweet_duration, "df_top_html": df_top_html,
                                                   "count_positive": count_positive, "count_neutral": count_neutral,
                                                   "count_negative": count_negative, "min_sentiment": min_sentiment,
                                                   "max_sentiment": max_sentiment, "std_sentiment": std_sentiment,
                                                   "chart": chart, "word_cloud": word_cloud, "hashtag_cloud": hashtag_cloud})


def Contact(request):
    return render(request, 'Contact.html', {})
