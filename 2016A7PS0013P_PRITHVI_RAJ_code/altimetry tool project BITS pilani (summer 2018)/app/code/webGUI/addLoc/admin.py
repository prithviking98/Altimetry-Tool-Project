from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Location)
admin.site.register(Kmz)
admin.site.register(ElevationGeoid)
admin.site.register(ElevationMss)
admin.site.register(Satellite)
admin.site.register(Country)
admin.site.register(WaterBodyType)
admin.site.register(State)
admin.site.register(Basin)