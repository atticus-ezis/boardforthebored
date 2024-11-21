from django import forms

# create form for city search 

# class CitySearch(forms.Form):
#     city = forms.CharField(
#         max_length=100,
#         label='',
#         widget=forms.TextInput(attrs={  # create widget to add class styling 
#             'class': 'custom-search-bar', # round corners, flex grow, margin etc 
#             'placeholder': 'Enter City',
#         })
#     )