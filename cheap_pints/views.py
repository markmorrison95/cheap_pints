from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from pip._vendor import requests

# Create your views here.
def index(request):
    TEMPLATE = 'cheap_pints/index.html'
    response = render(request, TEMPLATE, context={})
    return response

def barList(request):
    TEMPLATE = 'cheap_pints/bars.html'
    response = render(request, TEMPLATE, context={})
    return response

def geoLoc(request, value):
    key = 'AIzaSyBriJsnGZXUppVFg-q7cr2VpqHRmm7kczM'
    access_key = '397013fc76d5de24d0cc0b04b52e2aa6'
    latlng = value
    response2 = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+latlng+'&radius=1500&key='+key)
    nearby = response2.json()
    return render(request, 'cheap_pints/geolocation.html', {
        'result': nearby['results']
    })

