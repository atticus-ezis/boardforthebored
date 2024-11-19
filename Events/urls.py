from django.urls import path, include
from .views import *

app_name = 'events'

urlpatterns = [
    path('explore/', search_city, name='explore'),
    
    
]