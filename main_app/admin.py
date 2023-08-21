from django.contrib import admin
from .models import Itinerary, Destination, Chose_dest, Era, Photo

# Register your models here.
admin.site.register(Itinerary)
admin.site.register(Destination)
admin.site.register(Chose_dest)
admin.site.register(Era)
admin.site.register(Photo)

# all elements we will be able to crud within admin