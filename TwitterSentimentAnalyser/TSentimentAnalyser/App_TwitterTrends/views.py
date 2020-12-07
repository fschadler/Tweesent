from django.shortcuts import render
from App_TwitterDataCollector.forms import *

class GetLocationBasedTrends:

    def get_location_and_trends(self, request):  # input needs to be string
        geolocator = Nominatim(user_agent="TweetAnalyser")
        location = geolocator.geocode(request)
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
def trends_form_view(request):

    context = {}

    """
        Variables for HTML:
    """
    # Variable to display the location the user has entered.
    input_location = request.POST.get("location", None)
    context["input_location"] = input_location
    return render(request, 'home.html', context)

def FAQ(request):
    return render(request, 'FAQ.html', {})
