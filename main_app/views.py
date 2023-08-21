from django.shortcuts import render, redirect
# CBVs
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Models
from .models import Destination, Itinerary, Stop, Era, Photo
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
# Import the login_required decorator
from django.contrib.auth.decorators import login_required

# AB - home view
def home (request):
    return render(request, 'home.html')

# ------Itineraries (/itins/)---------------
# Itins_index
@login_required 
def itins_index(request):
  # Itins for logged in user
  itins = Itinerary.objects.filter(user=request.user)
  return render(request, 'itins/index.html', {
    'itins': itins
  })

# Itins_Detail
@login_required 
def itins_detail(request, itin_id):
  itin = Itinerary.objects.get(id=itin_id)
  # list of 'stops' associated with the an individual 'itinerary'
  # stops_a_user_has_added = itin.stop.all().values_list('id')

  return render(request, 'itins/detail.html', {
    'itin': itin,
    # 'stops': stops_a_user_has_added
  })

# createView
class ItinCreate(LoginRequiredMixin, CreateView):
  model = Itinerary
  fields = ['init_name',
            'itin_description',
            'init_travel_date', 
            'end_travel_date', 
            'user_budget'
            ]

  #overriding CBV properties to assign a user to a itinerary 
  def form_valid(self, form):
    # form.instance is the unsaved itin object / self.request.user is the logged in user object
    form.instance.user = self.request.user
    return super().form_valid(form)

# updateView
class ItinUpdate(LoginRequiredMixin, UpdateView):
  model = Itinerary
  fields = ['init_name',
            'itin_description',
            'init_travel_date', 
            'end_travel_date', 
            'user_budget'
            ]

# deleteView
class ItinDelete(LoginRequiredMixin, DeleteView):
  model = Itinerary
  success_url = '/itins'

# ------Stops (/itins/)--------------- 


#---------User--------------------------------
# Using Joel's updated way so that the username is prefilled in if error
def signup(request):
  error_message = ''
  form = UserCreationForm(request.POST)
  if request.method == 'POST':
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('itins_index')
    else:
      error_message = 'Invalid sign up - try again'
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# --------Destination (/dests/)---------------- 

def destinations_index(request, era_id):
  era = Era.objects.get(id=era_id)
  destinations = era.destination.all()
  return render(request, 'destinations/index.html', {
    'destinations': destinations,
  })