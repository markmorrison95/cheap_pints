from django.contrib import admin
from cheap_pints.models import Bar,Beer,PintPrice
# Register your models here.
admin.site.register(Bar)
admin.site.register(Beer)
admin.site.register(PintPrice)