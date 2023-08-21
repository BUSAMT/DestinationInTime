from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# user model is built in within django, so needs to be imported correctly

# Destination model
class Destination(models.Model):
    dest_name = models.CharField(max_length=150)
    dest_description = models.TextField(max_length=3000)
    dest_address = models.CharField(max_length=300)
    dest_country = models.CharField(max_length=100)
    price_range = models.CharField(max_length=100)

    def __str__(self):
        return self.dest_name

    def get_absolute_url(self):
        return reverse('dest_detail', kwargs={'pk': self.id})
    

# Era model
class Era(models.Model):
    era_name = models.CharField(max_length=250)
    era_peroid = models.CharField(max_length=200)
    era_description = models.TextField(max_length=2000)
    # M:M with Era
    destination = models.ManyToManyField(Destination)

    def __str__(self):
        return self.era_name


#  Itinerary model 
class Itinerary(models.Model):
    init_travel_date = models.DateField("Starting journey date")
    end_travel_date = models.DateField("Ending journey date")
    user_budget = models.IntegerField()
    itin_description = models.TextField(max_length=3000)
# user model built within django
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Journey from {self.init_travel_date} to {self.end_travel_date}"

    def get_absolute_url(self):
        return reverse('itins_detail', kwargs={'itinerary_id': self.id})
    


# Chosen destination model
class Stop(models.Model):
    dest_name = models.CharField(max_length=150)
    dest_description = models.CharField(max_length=3000)
    init_date_at_dest = models.DateField('Starting date at destination')
    end_date_at_dest = models.DateField('Ending date at destination')
    comments = models.TextField(max_length=3000)
# O:M with destination
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='stop_destin')
# O:M with itinerary
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='Itinerary_plan')

    def __str__(self):
        return f"{self.dest_name} from {self.init_date_at_dest} to {self.end_date_at_dest}"

    def get_absolute_url(self):
        return reverse('destinations_detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['-init_date_at_dest']


class Photo(models.Model):
    url = models.CharField(max_length=500)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for destination_id: {self.destination_id} @{self.url}"
