from django.shortcuts import render
from .forms import *
from .twitter_credentials import *
import tweepy
from geopy import Nominatim

"""
This app is used for authentication and filtering Tweets based on the user-input on the home-page. 
And searching for Trends based on User-Input in Location Form. 
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
        input_hashtag = request.POST['input_hashtag']
        input_num = int(request.POST['input_num'])
        twitter_client = TwitterClient()
        api = twitter_client.get_twitter_client_api()
        tweets = [status for status in tweepy.Cursor(api.search, q=input_hashtag).items(input_num)]
        return tweets


class TwitterAuthenticator:
    """
    Class to authenticate based on entries in twitter_credentials.
    """
    def authenticate_twitter_app(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


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
Displays the home.html where the user can input their hashtag, number of Tweets and location.
"""


def show(request):
    hashtag_form = HashtagForm()
    num_form = NumForm()
    location = LocationForm()

    # Checks whether location was submitted and renders the result, otherwise just displays standard home.html
    if request.POST.get("input_location") != None:
        input_location = request.POST.get("input_location")
        geolocator = Nominatim(user_agent="TweetAnalyser")
        # Looks for location based on input
        loc = geolocator.geocode(input_location)
        twitter_client = TwitterClient()
        api = twitter_client.get_twitter_client_api()
        location_data = api.trends_closest(loc.latitude, loc.longitude)
        # Where on earth ID based on Tweets
        woeid = location_data[0]["woeid"]
        # List of top 10
        top10_trends = []
        try:
            trends_results = api.trends_place(woeid)
            for trend in trends_results[0]["trends"][:10]:
                top10_trends.append(trend["name"])
        except tweepy.error.TweepError:
            return render(request, 'home.html', {'hashtag_form': hashtag_form, "num_form": num_form, 'location': location})
        return render(request, 'home.html', {'hashtag_form': hashtag_form, "num_form": num_form, 'location': location,
                                             'input_location': input_location, 'top10_trends': top10_trends})
    else:
        return render(request, 'home.html', {'hashtag_form': hashtag_form, "num_form": num_form, 'location': location})
