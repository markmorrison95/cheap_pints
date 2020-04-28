from django.urls import path
from cheap_pints import views
from cheap_pints.views import AddBar, AddBeer
from django.urls import include, re_path
from cheap_pints import search
app_name = 'cheap_pints'

urlpatterns = [
    path('', views.index, name='index'),
    path('bars/', views.barList, name='bars'),
    path('add_bar/', AddBar.as_view(), name='add_bar'),
    path('bar/<str:id>/', views.bar, name='bar' ),
    path('barsearch/', search.autocompleteBars, name='autocompleteBars'),
    path('beernamesearch/', search.autocompleteBeerNames, name='autocompleteBeerName'),
    path('beerbrandsearch/', search.autocompleteBeerBrands, name='autocompleteBeerBrands'),
    path('add_beer/<str:id>/', AddBeer.as_view(), name='add_beer'),
]