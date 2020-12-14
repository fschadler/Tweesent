from django import forms
from django.core.validators import RegexValidator

"""
Classes for forms on home-page. 
"""


class HashtagForm(forms.Form):
     """
     User Input on homepage which is used to filter tweet-search.
     """
     input_hashtag = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))


class NumForm(forms.Form):
    """
    User Input on homepage which is used to filter tweet-search.
    """
    input_num = forms.CharField(label='', widget=forms.NumberInput(
        attrs={"min": 1, "max": 500, "class": "form-control"}))


class LocationForm(forms.Form):
    """
    User Input on homepage which is used to show location-based trends.
    """
    input_location = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter City/Country', "class": "form-control"}))