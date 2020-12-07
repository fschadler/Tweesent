from django import forms
from django.core.validators import RegexValidator



class TwitterForm(forms.Form):
     """
     User Input on homepage which is used to filter tweet-search.
     """
     hashtag = forms.CharField(label='Hashtag or Word', max_length=30, widget=forms.TextInput
                                (attrs={'placeholder': '#Hashtag or SearchTerm'}))
     num_terms = forms.CharField(label='Number of Tweets', widget=forms.NumberInput(attrs={'placeholder': '100', "min": 1, "max": 500}))

class LocationForm(forms.Form):
    """
    User Input on homepage which is used to show location-based trends.
    """
    location = forms.CharField(label='Your location', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter City/Country'}))