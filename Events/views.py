import requests
import os

from django.shortcuts import render
from .models import *
from .forms import CitySearch

from django.http import JsonResponse
from collections import defaultdict


# pass city submit to api
def search_city(request):
    events = []
    grouped_events = []

    if request.method == 'POST':
        form = CitySearch(request.POST)
        if form.is_valid():
            # get city ** required
            city = form.cleaned_data['city']
            # get class filters if any -- else None
            class_name = request.POST.get('event_class', None)
            # get events in city
            events = get_events_by_city(city, class_name=class_name)
            # organize events by type
            grouped_events = get_events_by_type(events)
            # values passed 
            context = {
                'form': form,
                'grouped_events': grouped_events,
            }
    else:
        form = CitySearch()
        
    return render(request, 'explore_events.html', {'form':form, 'grouped_events':grouped_events})

# group city results by class
def get_events_by_type(events):
    groupby = defaultdict(list)
    for event in events:
        groupby[event['class']].append(event) 
    return dict(groupby)


# get JSON data
def get_events_by_city(city, **kwargs):
    events_dict = {}

    # connect to api
    api_key = os.getenv('TICKETMASTER_API_KEY')
    url = f"https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        'apikey': api_key,
        'city': city, 
        'includeSpellcheck':'yes',
        'radius': '50',
        'unit': 'miles',
        'size': 10, 
        'sort':'date,asc', 
    }

    # class param 
    if 'class_name' in kwargs and kwargs['class_name']:
        params['classificationName'] = kwargs['class_name']

    # date param
    if 'start_date' in kwargs and kwargs['start_date']:
        params['startDateTime'] = params['start_date']
    if 'end_date' in kwargs and kwargs['end_date']:
        params['endDateTime'] = params['start_date']



    # return JSON data as dictionary
    response = requests.get(url, params=params)
    if response.status_code == 200:
        events = response.json().get('_embedded', {}).get('events', []) 

        # iterate and select relevant data    
        for event in events:

            # date
            event_date = event.get('dates', {}).get('start', {}).get('localDate', [])
            # genre and classification
            if 'classifications' in event and event['classifications']:
                event_type = event['classifications'][0]
                
                if 'segment' in event_type:
                    event_segment_name = event_type.get('segment', {}).get('name', 'Something Unique')
                    if event_segment_name:
                        event['class'] = event_segment_name
                        if event_segment_name == "Undefined":
                            event['class'] = "Something Unique"
                    else:
                         event['class'] = 'Something Unique' 
                
                if 'genre' in event_type:
                    event['genre'] = event_type.get('genre', {}).get('name', 'Miscellaneous')
            else:
                event['class'] = "Something Unique"
                event['genre'] = 'Miscellaneous'
        
            images = event.get('images', [])
            if images:
                event['image_url'] = images[0]['url']

            if '_embedded' in event and 'venues' in event['_embedded']:
                venue = event['_embedded']['venues'][0]
                event['venue_name'] = venue.get('name', 'Unlisted')
                event['venue_city'] = venue.get('city', {}).get('name', 'Unlisted')

            if 'url' not in event:
                event['url'] = None
                

            

            # append events to dict with unique names 

            if event['name'] not in events_dict:
                events_dict[event['name']] = {
                    'name':event['name'], 
                    'image_url':event['image_url'], 
                    'dates':[event_date],
                    'venue':event['venue_name'], 
                    'venue_city':event['venue_city'], 
                    'info':event['url'],
                    'id':event['id'],
                    'class':event['class'],
                    'genre':event['genre'],
                   
                }

            else:
            # Append the new date if it's not already in the list
                if event_date and event_date not in events_dict[event['name']]['dates']:
                    events_dict[event['name']]['dates'].append(event_date)

        event_list = [
             {
                'name':event_data['name'], 
                'image_url':event_data['image_url'], 
                'dates':event_data['dates'], 
                'venue':event_data['venue'], 
                'venue_city':event_data['venue_city'], 
                'info':event_data['info'], 
                'id':event_data['id'],
                'class':event_data['class'],
                'genre':event_data['genre']
             }

             for event_data in events_dict.values() 
        ]

        return event_list 

    return []







# def get_events(request):
#     # Get the user query parameters from the request
#     date = request.GET.get('date')
#     location = request.GET.get('location')

#     # Define the base URL for the external API
#     eventbrite_url = 'https://www.eventbriteapi.com/v3/users/me/?token=77QGPDDQ6HHOKSY3SAO2'

#     # Define the API query parameters
#     params = {
#         'q': 'events',
#         'location.address': location,
#         'start_date.range_start': f'{date}T00:00:00',
#         'token': '',
#     }

#     # Make the request to the external API
#     response = requests.get(eventbrite_url, params=params)

#     # Check if the response is successful
#     if response.status_code == 200:
#         event_data = response.json()

#         # Return the data in JSON format to your frontend
#         return JsonResponse(event_data, safe=False)
#     else:
#         # Handle errors, return an appropriate error message
#         return JsonResponse({'error': 'Unable to fetch events'}, status=response.status_code)
    



