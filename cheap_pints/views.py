from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

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
    TEMPLATE = 'cheap_pints/geolocation.html'
    response = render(request, TEMPLATE, context={})
    return response

