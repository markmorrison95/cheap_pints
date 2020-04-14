from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from pip._vendor import requests
from cheap_pints.models import PintPrice

# Create your views here.
def index(request):
    TEMPLATE = 'cheap_pints/index.html'
    response = render(request, TEMPLATE, context={})
    return response

def barList(request, value):
    TEMPLATE = 'cheap_pints/bars.html'
    template_name = 'cheap_pints/bars.html'
    key = 'AIzaSyBriJsnGZXUppVFg-q7cr2VpqHRmm7kczM'
    access_key = '397013fc76d5de24d0cc0b04b52e2aa6'
    latlng = value
    latlng = str('55.873694,-4.283646') #value for bank street, use to force search area
    response2 = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+ latlng +'&&type=bar&rankby=distance&key='+key)
    nearby = response2.json()
    place_ids = extract_values(nearby, 'place_id')
    bars = []
    for place in place_ids:
        bars += PintPrice.objects.filter(googleId=place)
    context = {'bars':bars}
    return render(request, template_name, context)




def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
