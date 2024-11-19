from django.shortcuts import render
import requests
from django.http import JsonResponse
import os
username = os.getenv('GEONAMES_USERNAME')

def index_view(request):
    return render(request, 'test_index.html') 

def test_index_view(request):
    return render(request, 'test_index.html')

def city_autofill(request):
    city = request.GET.get('city', '')
    country = "US"
    if city:
        geonames_url = f"http://api.geonames.org/searchJSON?name_startsWith={city}&country={country}&maxRows=10&username={username}"
        response = requests.get(geonames_url)
        data = response.json().get('geonames', [])
        us_data = [item for item in data if item.get('countryCode') == 'US']
        suggestions = [
            {"city": item['name'], "state": item.get('adminCode1', '')}
            for item in data
        ]
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)

