from django import forms


class TwitterForm(forms.Form):
     """
     User Input on homepage which is used to filter tweet-search.
     """
     hashtag = forms.CharField(label='Hashtag', max_length=30, widget=forms.TextInput(attrs={'placeholder': '#Hashtag'}))
     num_terms = forms.CharField(label='Number of Tweets', widget=forms.NumberInput(attrs={'placeholder': '100', "min": 1, "max": 500}))

class LocationForm(forms.Form):
    """
    User Input on homepage which is used to show location-based trends.
    """
    location = forms.CharField(label='Your location', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter City/Country'}))