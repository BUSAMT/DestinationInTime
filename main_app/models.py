from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# user model is built in within django, so needs to be imported correctly



# DESTINATION MODEL
class Destination(models.Model):
    destName = models.CharField(max_length=150)
    destDescription = models.CharField(max_length=500)
    destAddress = models.CharField(max_length=300)
    destCountry = models.CharField(max_length=20)
    priceRange = models.CharField(max_length=20)

    def some_method(self):
        from .models import Itinerary
        itineraries = models.ManyToManyField(Itinerary)

    def __str__(self):
        return self.destName

    def get_absolute_url(self):
        return reverse('destinations_detail', kwargs={'pk': self.id})

  
class Itinerary(models.Model):
    dateTravel = models.DateTimeField(("Travel Date"), auto_now=False, auto_now_add=False)
    userBudget = models.IntegerField
    description = models.TextField(max_length=500)

    destinations = models.ManyToManyField(Destination)

    def some_other_method(self):
        from .models import Destination
        # You can use the Destination model here

    # Correct the indentation for the following fields
    chosDest = models.ForeignKey('ChosDest', on_delete=models.CASCADE, related_name='itinerary_for')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.dateTravel} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'itinerary_id': self.id})

class ChosDest(models.Model):
    destName = models.CharField(max_length=150)
    destDescription = models.CharField(max_length=500)
    dateAtDest = models.DateField()
    comments = models.CharField(max_length=20)

    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='chos_destinations')

    def __str__(self):
        return self.destName

    def get_absolute_url(self):
        return reverse('destinations_detail', kwargs={'pk': self.id})

class Era(models.Model):
    eraName = models.CharField(max_length=250)
    eraPeroid = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    destinations = models.ManyToManyField(Destination)

    def __str__(self):
        return self.eraName

class Photo(models.Model):
    url = models.CharField(max_length=500)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for destination_id: {self.destination_id} @{self.url}"
