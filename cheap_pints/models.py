from django.db import models

# Create your models here.
class Bar(models.Model):

    """A model for a print price."""

    NAME_MAX_LENGTH = 128
    URL_MAX_LENGTH = 255
    UNIT_MAX_LENGTH = 12

    POUND = '£'
    DOLLAR = '$'
    EURO = '€'
    PRICE_UNITS = (
        (1,POUND),
        (2,DOLLAR),
        (3,EURO),
    )

    # Reference Fields
    # ----------------
    bar_id = models.AutoField(primary_key=True,auto_created=True)
    googleId = models.CharField(max_length=NAME_MAX_LENGTH)
    barName = models.CharField(max_length=NAME_MAX_LENGTH)
    price = models.FloatField(blank=False)
    price_unit = models.CharField(max_length=UNIT_MAX_LENGTH,default=POUND, choices=PRICE_UNITS)
    image_reference = models.CharField(max_length=URL_MAX_LENGTH, blank=True)
    # Date and time created
    created_date = models.DateTimeField(auto_now_add=True)
    # The owning user
    # on_delete: When the user is deleted, all their meals are deleted
    def __str__(self): return self.barName



class PintPrice(models.Model):

    """A model for a print prices."""

    POUND = '£'
    DOLLAR = '$'
    EURO = '€'
    PRICE_UNITS = (
        (1,POUND),
        (2,DOLLAR),
        (3,EURO),
    )
    UNIT_MAX_LENGTH = 1

    # Reference Fields
    # ----------------
    id = models.AutoField(primary_key=True,auto_created=True)
    BeerTypeId = models.ForeignKey('Beer', related_name='PintPriceBeerId', on_delete=models.CASCADE)
    googleId = models.ForeignKey('Bar', related_name='PrintPriceGoogleId', on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    price_unit = models.CharField(max_length=UNIT_MAX_LENGTH,default=POUND, choices=PRICE_UNITS)
    # Date and time created
    created_date = models.DateTimeField(auto_now_add=True)
    # The owning user
    # on_delete: When the user is deleted, all their meals are deleted
    def __str__(self): return self.barGoogleId

class Beer(models.Model):

    NAME_MAX_LENGTH = 128

    """ Creates a model bor beers so beers will be serachable across all bars """
    id = models.AutoField(primary_key=True,auto_created=True)
    BeerName = models.CharField(unique=True, max_length=NAME_MAX_LENGTH)
    BeerBrand = models.CharField(unique=True, max_length=NAME_MAX_LENGTH, blank=True)
    
    def __str__(self): return self.BeerName