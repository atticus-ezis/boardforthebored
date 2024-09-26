import requests
import os

from django.shortcuts import render
from .models import *
from django.http import JsonResponse



# pass city submit to api
def search_events(request):
    events = []
    if request.method == 'POST':
        form = CitySearch(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            events = get_events_by_city(city)  # Fetch events using API
    else:
        form = CitySearch()

    return render(request, 'events/explore_events.html', {'form': form, 'events': events})

# api connection 
def get_events_by_city(city):
    api_key = os.getenv('TICKETMASTER_API_KEY')
    url = f"https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        'apikey': api_key,
        'city': city, 
        'includeSpellcheck':'yes',
        'radius': '50',
        'unit': 'miles',
        'size': 10,  # Number of events to fetch (you can change this)
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('_embedded', {}).get('events', [])
    return []

def Explore(request):
    return render(request, 'explore_events.html')

def get_events(request):
    # Get the user query parameters from the request
    date = request.GET.get('date')
    location = request.GET.get('location')

    # Define the base URL for the external API
    eventbrite_url = 'https://www.eventbriteapi.com/v3/users/me/?token=77QGPDDQ6HHOKSY3SAO2'

    # Define the API query parameters
    params = {
        'q': 'events',
        'location.address': location,
        'start_date.range_start': f'{date}T00:00:00',
        'token': '',
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
    



