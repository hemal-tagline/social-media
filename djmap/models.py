from django.db import models

# Create your models here.

from django.db import models 
from mapbox_location_field.models import LocationField


class SomeLocationModel(models.Model):
    destination_latitude = models.DecimalField(max_digits=50, decimal_places=15)
    destination_longitude = models.DecimalField(max_digits=50, decimal_places=15)
    location = LocationField()

