from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self): return self.name
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
    googleId = models.CharField(max_length=NAME_MAX_LENGTH,primary_key=True)
    barName = models.CharField(max_length=NAME_MAX_LENGTH)
    image_reference = models.CharField(max_length=URL_MAX_LENGTH, blank=True)
    # Date and time created
    created_date = models.DateTimeField(auto_now_add=True)
    # slug = models.SlugField(unique=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    # The owning user
    # on_delete: When the user is deleted, all their meals are deleted
    def save(self, *args, **kwargs):
        # self.slug = slugify(self.barName +'_'+ self.city.name)
        super(Bar, self).save(*args,**kwargs)


    def __str__(self): return self.barName

class Beer(models.Model):

    NAME_MAX_LENGTH = 128

    """ Creates a model bor beers so beers will be searchable across all bars """
    id = models.AutoField(primary_key=True,auto_created=True)
    BeerName = models.CharField(unique=True, max_length=NAME_MAX_LENGTH)
    BeerBrand = models.CharField(unique=False, max_length=NAME_MAX_LENGTH, blank=True)
    
    def __str__(self): return self.BeerName



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
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    price_unit = models.IntegerField(default=POUND, choices=PRICE_UNITS)
    # Date and time created
    created_date = models.DateTimeField(auto_now_add=True)
    # The owning user
    # on_delete: When the user is deleted, all their meals are deleted

    class Meta:
        unique_together = (("beer", "bar"),)

    def __str__(self): 
        return self.bar.barName + ': ' + self.beer.BeerName
    
    def price_unit_verbose(self):
        return dict(PintPrice.PRICE_UNITS)[self.price_unit]