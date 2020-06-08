from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from pip._vendor import requests
from cheap_pints.models import Bar, Beer, City, PintPrice
from cheap_pints.forms import BarForm, BeerForm, CityForm, PintPriceForm
from django.urls import reverse
from django.http import HttpResponse
import json
from find_my_pint_project.settings import GOOGLE_APP_KEY

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.



def index(request):
    key = GOOGLE_APP_KEY
    TEMPLATE = 'cheap_pints/index.html'
    response = render(request, TEMPLATE, context={'api_key':key})
    return response

def google(request):
    TEMPLATE = 'cheap_pints/geolocation.html'
    response = render(request, TEMPLATE, context={})
    return response

def barList(request):
    template = 'cheap_pints/bars.html'
    key = GOOGLE_APP_KEY
    try:
        barname = request.GET['barname']
        barname=barname.replace("+", " ")
        bars = Bar.objects.filter(barName__iexact=barname)
        PintPrices = []
        for bar in bars:
            PintPrices += PintPrice.objects.filter(bar=bar).order_by('price')[:1]
        context = {'PintPrices':PintPrices,
                    'api_key':key,
                    'search_type':'Bars Named '+barname+':'}
        return render(request, template, context)

    except:
        lat = request.GET['lat']
        lng = request.GET['lng']
        # latlng = str('55.873694,-4.283646') #value for bank street, use to force search area
        response2 = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat +','+lng+'&&type=bar&rankby=distance&key='+key)
        nearby = response2.json()
        place_ids = extract_values(nearby, 'place_id')
        bars = []
        PintPrices = []
        for place in place_ids:
            bars += Bar.objects.filter(googleId=place)
        for bar in bars:
            PintPrices += PintPrice.objects.filter(bar=bar).order_by('price')[:1]
        context = {'PintPrices':PintPrices,
                    'api_key':key,
                    'search_type':'Bars Near You:'}
        return render(request, template, context)

def bar(request, id):
    template = 'cheap_pints/bar.html'
    key = GOOGLE_APP_KEY
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

class AddBar(LoginRequiredMixin, View):
    """ A view for adding a meal to the database """

    TEMPLATE = "cheap_pints/addBar.html"
    key = GOOGLE_APP_KEY

    # @method_decorator(login_required)
    def get(self, request, meal_id_slug=None):
        """ Display the form for adding / editing a meal """

        barForm = BarForm()
        beerForm = BeerForm()
        pintPriceForm = PintPriceForm()
        cityForm = CityForm()

        return render(request, self.TEMPLATE, context={
            'api_key': self.key,
            'BarForm': barForm,
            'BeerForm': beerForm,
            'PintPriceForm': pintPriceForm,
            'CityForm':cityForm,
        })


    def post(self, request):
        """ Process the form submitted by the user """

        # If there's a meal slug, supply the instance
        barForm = BarForm(request.POST)
        beerForm = BeerForm(request.POST)
        pintPriceForm = PintPriceForm(request.POST)
        cityForm = CityForm(request.POST)
        print(request.POST)
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

        if cityForm.is_valid():
            city, created = City.objects.get_or_create(name=request.POST.get('city'))
        else:
            print(cityForm.errors)
        if (barExists or barForm.is_valid()) and (beerExists or beerForm.is_valid()) and pintPriceForm.is_valid():
            if not barExists:
                bar = barForm.save(commit=False)
                placeId = bar.googleId
                response = requests.get('https://maps.googleapis.com/maps/api/place/details/json?place_id='+ placeId +'&fields=photo&key=' + self.key)
                photo = response.json()
                ref =  extract_values(photo,'photo_reference')
                if len(ref)>0:
                    bar.image_reference = ref[0]
                bar.city = city      
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
            'api_key': self.key,
            'BarForm': barForm,
            'BeerForm': beerForm,
            'PintPriceForm': pintPriceForm,
        })


class AddBeer(LoginRequiredMixin, View):
    """ A view for a beer to and """

    TEMPLATE = "cheap_pints/addBeer.html"
    key = GOOGLE_APP_KEY

    # @method_decorator(login_required)
    def get(self, request, id):
        """ Display the form for adding / editing a meal """

        bar = Bar.objects.get(googleId=id)
        beerForm = BeerForm()
        pintPriceForm = PintPriceForm()

        return render(request, self.TEMPLATE, context={
            'bar': bar,
            'BeerForm': beerForm,
            'PintPriceForm': pintPriceForm,
            'api_key': AddBeer.key,
        })


    def post(self, request, id):
        """ Process the form submitted by the user """

        # If there's a meal slug, supply the instance
        bar = Bar.objects.get(googleId=id)
        beerForm = BeerForm(request.POST)
        pintPriceForm = PintPriceForm(request.POST)
        beerExists = True
        try:
            beer = Beer.objects.get(BeerName=request.POST.get('BeerName'))
        except Beer.DoesNotExist:
            beerExists = False

        if (beerExists or beerForm.is_valid()) and pintPriceForm.is_valid():
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
            print(beerForm.errors)
            return render(request, self.TEMPLATE, context={
            'bar': bar,
            'BeerForm': beerForm,
            'PintPriceForm': pintPriceForm,
            'api_key': AddBeer.key,
        })
