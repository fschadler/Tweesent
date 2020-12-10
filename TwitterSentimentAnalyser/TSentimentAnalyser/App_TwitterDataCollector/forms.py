from django import forms
from django.core.validators import RegexValidator



class TwitterForm(forms.Form):
     """
     User Input on homepage which is used to filter tweet-search.
     """
     hashtag = forms.CharField(label='Hashtag or Word', max_length=30, widget=forms.TextInput
                                (attrs={'placeholder': '#Sentiment', "class": "form-control"}))
     num_terms = forms.CharField(label='Number of Tweets', widget=forms.NumberInput(attrs={'placeholder': '100',"min": 1, "max": 500, "class": "form-control"}))

class LocationForm(forms.Form):
    """
    User Input on homepage which is used to show location-based trends.
    """
    location = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter City/Country', "class": "form-control"}))