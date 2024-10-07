from django import forms

class CitySearch(forms.Form):
    city = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'custom-search-bar', 
            'placeholder': 'Enter City',
        })
    )