from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from cheap_pints.models import Bar, Beer, PintPrice
from cheap_pints.forms import BarForm, BeerForm, PintPriceForm
from django.urls import reverse
from django.http import HttpResponse
import json






def autocompleteBars(request):
    try: 
        search_query = request.GET['BarSearch']
        bars = Bar.objects.filter(barName__iexact=search_query)
        if len(bars) == 1:
            return redirect(reverse('cheap_pints:bar', kwargs={'id':bars[0].googleId,
                                                                'slug':bars[0].slug}))
        else:
            search_query=search_query.replace(" ", "+")
            return redirect('/cheap_pints/bars/?barname='+search_query)

    except:
        search_qs = Bar.objects.filter(barName__icontains=request.GET['search'])
        results = []
        for r in search_qs:
            results.append(r.barName)
        resp = request.GET['callback'] + '(' + json.dumps(results) + ');'
        return HttpResponse(resp, content_type='application/json')

def autocompleteBeerNames(request):
    search_query = Beer.objects.filter(BeerName__icontains=request.GET['search'])
    results = []
    for r in search_query:
        results.append(r.BeerName)
    resp = request.GET['callback'] + '(' + json.dumps(results) + ');'
    return HttpResponse(resp, content_type='application/json')

def autocompleteBeerBrands(request):
    search_query = Beer.objects.filter(BeerBrand__icontains=request.GET['search'])
    results = []
    for r in search_query:
        results.append(r.BeerBrand)
    resp = request.GET['callback'] + '(' + json.dumps(results) + ');'
    return HttpResponse(resp, content_type='application/json')