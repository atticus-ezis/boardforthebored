from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django_filters.rest_framework import DjangoFilterBackend
import requests
from django.http import JsonResponse
from django.conf import settings

EVENTBRITE_API_KEY = 'your_eventbrite_api_key'

def Explore(request):
    return render(request, 'explore_events.html')

def get_events(request):
    # Get the user query parameters from the request
    date = request.GET.get('date')
    location = request.GET.get('location')

    # Define the base URL for the external API
    eventbrite_url = 'https://www.eventbriteapi.com/v3/events/search/'

    # Define the API query parameters
    params = {
        'q': 'events',
        'location.address': location,
        'start_date.range_start': f'{date}T00:00:00',
        'token': EVENTBRITE_API_KEY,
    }

    # Make the request to the external API
    response = requests.get(eventbrite_url, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        event_data = response.json()

        # Return the data in JSON format to your frontend
        return JsonResponse(event_data, safe=False)
    else:
        # Handle errors, return an appropriate error message
        return JsonResponse({'error': 'Unable to fetch events'}, status=response.status_code)

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'location']