from django.shortcuts import render
from .forms import *
from .twitter_credentials import *
import tweepy

"""
This app is used for authentication and filtering Tweets based on the user-input on the home-page. 
"""


class TwitterClient:
    """
    Uses Authenticator Class to pull tweets based on user input.
    """
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = tweepy.API(self.auth)

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_tweets(self, request):
        t = request.POST['hashtag']
        n = int(request.POST['num_terms'])
        twitter_client = TwitterClient()
        api = twitter_client.get_twitter_client_api()
        tweets = [status for status in tweepy.Cursor(api.search, q=t).items(n)]
        return tweets


class TwitterAuthenticator:
    """
    Class to authenticate based on entries in twitter_credentials.
    """
    def authenticate_twitter_app(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer:
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename):
        # This handles Twitter authentication and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = tweepy.Stream(auth, listener)


class TwitterListener(tweepy.StreamListener):
    """
    Class to print received tweets to stdout and closes connection if error occurs.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


"""
Displays the home.html where a user can input their hashtag and number of Tweets.
"""


def show(request):
    form = TwitterForm()
    return render(request, 'home.html', {'ff': form})
