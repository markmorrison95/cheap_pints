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


class allBars(TemplateView):
    """ A view for viewing all meals """

    template_name = 'cheap_pints/bars.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    def get_context_data(self):
        bars = PintPrice.objects.all().order_by('price')
        # Get tag slug (has to be this way for TemplateView)
        # tag_slug = self.kwargs.get('tag_slug', None)

        # if(tag_slug):
        #     try:
        #         # Filter meals by tag
        #         tag = Tag.objects.get(slug=tag_slug)
        #         context['tag'] = tag
        #         meals = meals.filter(tags__name__in=[tag.name])
        #     except Tag.DoesNotExist:
        #         # Signal in context_dict so an error message can be displayed
        #         # Will just display every meal regardless
        #         context['tag_slug'] = tag_slug
        #         context['tag_error'] = True

        # Pin most recent meals
        context = {'bars':bars}

        return context

