from django.shortcuts import render
from geopy.geocoders import Nominatim
import tweepy
from TwitterSentimentAnalyser.TSentimentAnalyser.App_TwitterDataCollector.views import TwitterClient

def get_location_and_trends(your_location):  # input needs to be string
    geolocator = Nominatim(user_agent="TweetAnalyser")
    location = geolocator.geocode(your_location)
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    location_data = api.trends_closest(location.latitude, location.longitude)
    woeid = location_data[0]["woeid"]
    try:
        trends_results = api.trends_place(woeid)
        for trend in trends_results[0]["trends"][:10]:
            print(trend["name"])
    except tweepy.error.TweepError:
        print("There are no trending topics in your location.")


# Create your views here.
