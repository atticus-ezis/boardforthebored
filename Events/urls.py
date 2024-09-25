from django.urls import path, include
from .views import Explore, EventListView

app_name = 'events'

urlpatterns = [
    path('explore/', Explore, name='explore'),
    path('events/', EventListView.as_view(), name='event-list'),
    
]