from django.urls import path
from cheap_pints import views

app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    path('bars/', views.barList, name='bars')
]