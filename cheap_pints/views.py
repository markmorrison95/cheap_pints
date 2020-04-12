from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from pip._vendor import requests
from django.contrib.gis.utils import GeoIP

# Create your views here.
def index(request):
    TEMPLATE = 'cheap_pints/index.html'
    response = render(request, TEMPLATE, context={})
    return response

def barList(request):
    TEMPLATE = 'cheap_pints/bars.html'
    response = render(request, TEMPLATE, context={})
    return response

def geoLoc(request):
    key = 'AIzaSyBriJsnGZXUppVFg-q7cr2VpqHRmm7kczM'
    access_key = '397013fc76d5de24d0cc0b04b52e2aa6'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    ip_address = '86.137.37.113'
    g = GeoIP()
    ip = request.META.get('REMOTE_ADDR', None)
    if ip:
        city = g.city(ip)['latitude']
        city = g.city(ip)['longitude']
    response = requests.get('http://api.ipstack.com/'+ip_address+'?access_key='+access_key+'&output=json')
    geodata = response.json()
    lat = str(geodata['latitude'])
    lng = str(geodata['longitude'])
    print(lat + ',' + lng)
    response2 = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat+','+lng+'&radius=1500&key='+key)
    nearby = response2.json()
    print(nearby)
    return render(request, 'cheap_pints/geolocation.html', {
        'result': nearby['results']
    })

