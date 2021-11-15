from django.contrib import admin

# Register your models here.
from .models import SomeLocationModel
from mapbox_location_field.admin import MapAdmin

admin.site.register(SomeLocationModel, MapAdmin)
