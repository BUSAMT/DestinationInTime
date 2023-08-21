from django.contrib import admin
from .models import Itinerary, Destination, Stop, Era, Photo

# Register your models here.
admin.site.register(Itinerary)
admin.site.register(Destination)
admin.site.register(Stop)
admin.site.register(Era)
admin.site.register(Photo)

# all elements we will be able to crud within admin