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

#  Itinerary model 
class Itinerary(models.Model):
    init_travel_date = models.DateField("Starting journey date")
    end_travel_date = models.DateField("Ending journey date")

    # initial-end travel date if not a
    user_budget = models.IntegerField()
    itin_description = models.TextField(max_length=3000)

    destinations = models.ManyToManyField(Destination)

    chose_dest = models.ForeignKey('Chose_dest', on_delete=models.CASCADE, related_name='itin_for')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Journey from {self.init_travel_date} to {self.end_travel_date}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'itinerary_id': self.id})
    


# Chosen destination model
class Chose_dest(models.Model):
    dest_name = models.CharField(max_length=150)
    dest_description = models.CharField(max_length=3000)
    init_date_at_dest = models.DateField('Starting date at destination')
    end_date_at_dest = models.DateField('Ending date at destination')
    comments = models.TextField(max_length=3000)

    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='chosen_destin')

    def __str__(self):
        return f"{self.dest_name} from {self.init_date_at_dest} to {self.end_date_at_dest}"

    def get_absolute_url(self):
        return reverse('destinations_detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['-init_date_at_dest']


# Era model
class Era(models.Model):
    era_name = models.CharField(max_length=250)
    era_peroid = models.CharField(max_length=200)
    era_description = models.TextField(max_length=2000)

    destinations = models.ManyToManyField(Destination)

    def __str__(self):
        return self.era_name



class Photo(models.Model):
    url = models.CharField(max_length=500)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for destination_id: {self.destination_id} @{self.url}"
