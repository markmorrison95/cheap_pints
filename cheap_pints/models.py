from django.db import models

# Create your models here.
class Bars(models.Model):

    """A model for a print price."""

    NAME_MAX_LENGTH = 128
    URL_MAX_LENGTH = 255
    UNIT_MAX_LENGTH = 12

    PRICE_DEFAULT_UNIT = '£'

    # Reference Fields
    # ----------------
    bar_id = models.AutoField(primary_key=True,auto_created=True)
    googleId = models.CharField(max_length=NAME_MAX_LENGTH)
    barName = models.CharField(max_length=NAME_MAX_LENGTH)
    price = models.FloatField(blank=False)
    price_unit = models.CharField(max_length=UNIT_MAX_LENGTH,default=PRICE_DEFAULT_UNIT)
    image_reference = models.CharField(max_length=URL_MAX_LENGTH, blank=True)
    # Date and time created
    created_date = models.DateTimeField(auto_now_add=True)
    # The owning user
    # on_delete: When the user is deleted, all their meals are deleted
    def __str__(self): return self.barName



class PintPrices(models.Model):

    """A model for a print prices."""

    PRICE_DEFAULT_UNIT = '£'
    UNIT_MAX_LENGTH = 1

    # Reference Fields
    # ----------------
    id = models.AutoField(primary_key=True,auto_created=True)
    BeerTypeId = models.ForeignKey('Beers', related_name='PintPriceBeerId', on_delete=models.CASCADE)
    googleId = models.ForeignKey('Bars', related_name='PrintPriceGoogleId', on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    price_unit = models.CharField(max_length=UNIT_MAX_LENGTH,default=PRICE_DEFAULT_UNIT)
    # Date and time created
    created_date = models.DateTimeField(auto_now_add=True)
    # The owning user
    # on_delete: When the user is deleted, all their meals are deleted
    def __str__(self): return self.barGoogleId

class Beers(models.Model):

    NAME_MAX_LENGTH = 128

    """" Creates a model bor beers so beers will be serachable across all bars """
    id = models.AutoField(primary_key=True,auto_created=True)
    BeerName = models.CharField(unique=True, max_length=NAME_MAX_LENGTH)