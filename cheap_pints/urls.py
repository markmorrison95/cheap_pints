from django.urls import path
from cheap_pints import views
from cheap_pints.views import AddBar
app_name = 'cheap_pints'

urlpatterns = [
    path('', views.index, name='index'),
    path('bars/<str:value>/', views.barList, name='bars'),
    path('add_bar/', AddBar.as_view(), name='add_bar'),
    path('bar/<str:id>/', views.bar, name='bar' ),
    path('search/', views.autocompleteModel, name='autocomplete')
]