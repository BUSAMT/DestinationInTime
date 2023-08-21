from django.shortcuts import render, redirect
# CBVs
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Models
from .models import Destination, Itinerary, Chose_dest, Era, Photo

# AB - home view
def home (request):
    return render(request, 'home.html')

# ------Itineraries (/itins/)--------------- 
# Itins_index 
def itins_index(request):
  # Itins for logged in user
  itins = Itinerary.objects.filter(user=request.user)
  return render(request, 'itins/index.html', {
    'itins': itins
  })

# Itins_Detail
def itins_detail(request, itinerary_id):
  itin = Itinerary.objects.get(id=itinerary_id)

  return render(request, 'itins/detail.html', {
    'itins': itin
    # pass through destination
    #  
  })

# createView
class ItinCreate(CreateView):
  model = Itinerary
  field = '__all__'

# updateView
class ItinUpdate(UpdateView):
  model = Itinerary
  fields = '__all__'

# deleteView
class ItinDelete(DeleteView):
  model = Itinerary
  success_url = '/itins'

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

