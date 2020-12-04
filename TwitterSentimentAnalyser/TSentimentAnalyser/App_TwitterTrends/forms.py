from django import forms


class LocationForm(forms.Form):
    """
    User Input on homepage which is used to show location-based trends.
    """
    location = forms.CharField(label='Your location', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter City/Country'}))