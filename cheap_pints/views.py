from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from pip._vendor import requests
from cheap_pints.models import Bar, Beer, PintPrice
from cheap_pints.forms import BarForm, BeerForm, PintPriceForm
from django.urls import reverse
from django.http import HttpResponse
import json

# Create your views here.
def autocompleteModel(request):
    search_qs = Bar.objects.filter(barName__icontains=request.GET['search'])
    results = []
    for r in search_qs:
        results.append(r.barName)
    resp = request.GET['callback'] + '(' + json.dumps(results) + ');'
    return HttpResponse(resp, content_type='application/json')


def index(request):
    TEMPLATE = 'cheap_pints/index.html'
    response = render(request, TEMPLATE, context={})
    return response

def google(request):
    TEMPLATE = 'cheap_pints/geolocation.html'
    response = render(request, TEMPLATE, context={})
    return response

def barList(request, value):
    TEMPLATE = 'cheap_pints/bars.html'
    template_name = 'cheap_pints/bars.html'
    key = 'AIzaSyBriJsnGZXUppVFg-q7cr2VpqHRmm7kczM'
    latlng = value
    # latlng = str('55.873694,-4.283646') #value for bank street, use to force search area
    response2 = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+ latlng +'&&type=bar&rankby=distance&key='+key)
    nearby = response2.json()
    place_ids = extract_values(nearby, 'place_id')
    bars = []
    PintPrices = []
    for place in place_ids:
        bars += Bar.objects.filter(googleId=place)
    for bar in bars:
        PintPrices += PintPrice.objects.filter(bar=bar).order_by('price')[:1]
    context = {'PintPrices':PintPrices,
                'api_key':key}
    return render(request, template_name, context)

def bar(request, id):
    template = 'cheap_pints/bar.html'
    key = 'AIzaSyBriJsnGZXUppVFg-q7cr2VpqHRmm7kczM'
    bar = Bar.objects.get(googleId=id)
    beers = PintPrice.objects.filter(bar=bar)
    context = {'bar':bar,
                'beers':beers,
                'api_key':key}
    return render(request, template, context)



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

class AddBar(View):
    """ A view for adding a meal to the database """

    TEMPLATE = "cheap_pints/addBar.html"

    # @method_decorator(login_required)
    def get(self, request, meal_id_slug=None):
        """ Display the form for adding / editing a meal """

        barForm = BarForm()
        beerForm = BeerForm()
        pintPriceForm = PintPriceForm()

        return render(request, self.TEMPLATE, context={
            'BarForm': barForm,
            'BeerForm': beerForm,
            'PintPriceForm': pintPriceForm,
        })


    def post(self, request):
        """ Process the form submitted by the user """

        # If there's a meal slug, supply the instance
        barForm = BarForm(request.POST)
        beerForm = BeerForm(request.POST)
        pintPriceForm = PintPriceForm(request.POST)
        barExists = True
        beerExists = True
        try:
            bar = Bar.objects.get(googleId=request.POST.get('googleId'))
        except Bar.DoesNotExist:
            barExists = False

        try:
            beer = Beer.objects.get(BeerName=request.POST.get('BeerName'))
        except Beer.DoesNotExist:
            beerExists = False

        if (barExists or barForm.is_valid()) and (beerExists or beerForm.is_valid()) and pintPriceForm.is_valid():
            if not barExists:
                bar = barForm.save(commit=False)
                key = 'AIzaSyBriJsnGZXUppVFg-q7cr2VpqHRmm7kczM'
                placeId = bar.googleId
                response = requests.get('https://maps.googleapis.com/maps/api/place/details/json?place_id='+ placeId +'&fields=photo&key=' + key)
                photo = response.json()
                ref =  extract_values(photo,'photo_reference')
                if len(ref)>0:
                    bar.image_reference = ref[0]             
                bar.save()

            if not beerExists:
                beer = beerForm.save()
            try:
                pintPrice = PintPrice.objects.get(bar=bar,beer=beer)
                pintPriceForm = PintPriceForm(request.POST,
                            instance=pintPrice)
                pintPrice = pintPriceForm.save()
            except PintPrice.DoesNotExist:
                pintPrice = pintPriceForm.save(commit=False)
                pintPrice.bar = bar
                pintPrice.beer = beer
                pintPrice.save()

            # Redirect to my_meals page
            return redirect(reverse('cheap_pints:bar', kwargs={'id':bar.googleId}))

        else:
            print(pintPriceForm.errors)
            print(barForm.errors)
            print(beerForm.errors)
            return render(request, self.TEMPLATE, context={
            'BarForm': barForm,
            'BeerForm': beerForm,
            'PintPriceForm': pintPriceForm,
        })


# url to get info from place_id
        # https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name,rating,formatted_phone_number&key=YOUR_API_KEY
