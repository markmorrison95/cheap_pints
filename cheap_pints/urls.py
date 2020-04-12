from django.urls import path
from cheap_pints import views
from cheap_pints.views import allBars
app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    path('bars/', allBars.as_view(), name='bars'),
    path('geo/<str:value>/', views.geoLoc, name='geo')
]