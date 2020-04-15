from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from pip._vendor import requests
from cheap_pints.models import PintPrice
from cheap_pints.forms import PintPriceForm

# Create your views here.
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
    for place in place_ids:
        bars += PintPrice.objects.filter(googleId=place)
    context = {'bars':bars,
            'api_key':key}
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

class AddBar(View):
    """ A view for adding a meal to the database """

    TEMPLATE = "cheap_pints/addBar.html"

    # @method_decorator(login_required)
    def get(self, request, meal_id_slug=None):
        """ Display the form for adding / editing a meal """

        # If the user is trying to edit a pre-existing meal
        # if(bar_id_slug):
        #     # 404 if no meal found
        #     mealget = get_object_or_404(Meal, id=meal_id_slug)
        #     user = request.user

        #     # Forbidden page if they are not the owner of the meal
        #     # to avoid hax...
        #     if (mealget.owner != user.userprofile):
        #         return HttpResponseForbidden()
        #     else:
                # Otherwise, fill the form in with the meal and return

                # Parse the tag fields to a comma separated list to populate
                # the input field. Necessary for the JQuery plugin

        form = PintPriceForm()

        return render(request, self.TEMPLATE, context={
            'form': form,
        })
