from django.db import models

# Create your models here.
class PintPrice(models.Model):

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
    # owner = models.ForeignKey(UserProfile,
    #                           on_delete=models.CASCADE,
    #                           related_name='%(class)s_owner')

    # This needs to be enforced to have MIN: 1 in the forms field
    def __str__(self): return self.barName