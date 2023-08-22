# the following imports are for AWS
import os
import uuid
import boto3

from django.shortcuts import get_object_or_404, render, redirect
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
# Form imports
from .forms import AddStopForm, ItinCreateForm

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
    form_class = ItinCreateForm 
    # created a custom form for the stupid date thing that was bothering me

  #overriding CBV properties to assign a user to a itinerary 
    def form_valid(self, form):
      # form.instance is the unsaved itin object / self.request.user is the logged in user object
      form.instance.user = self.request.user
      return super().form_valid(form)


# updateView
class ItinUpdate(LoginRequiredMixin, UpdateView):
    model = Itinerary
    form_class = ItinCreateForm  # Using the custom form for updating

    def form_valid(self, form):
        return super().form_valid(form)



# deleteView
class ItinDelete(LoginRequiredMixin, DeleteView):
  model = Itinerary
  success_url = '/itins'

# ------Stops (/itins/)--------------- 
# Create the form
@login_required
# def add_a_stop(request, itin_id):
#   # itinerary = Itininerary.objects.get(id=itin_id)
#   eras = Era.objects.all()
#   destination = Destination.objects.get(id=destination_id)
  
#   form = StopForm(request.POST)

#   if form.is_valid():
#     # display all eras_linked_to_destination
#     new_spot = form.save(commit=False)
#     # assoc with itin
#     new_spot.itinerary_id = itin_id
#     new_spot.destination_id = destination.id
#     new_spot.save()
#     return redirect('itins_detail', itin_id=itin_id)

#   return render(request,'itins/add_stop.html', {
#   'form': form,
#   'eras' : eras
#   })

# change from assoc with itin to assoc with dest icluding url and temaplte
# def add_a_stop(request, itin_id,):
#   form = StopForm(request.POST)
#   eras = Era.objects.all()

#   if form.is_valid():
#     # display all eras_linked_to_destination
#     new_spot = form.save(commit=False)
#     # assoc with itin
#     new_spot.itinerary_id = itin_id
#     new_spot.save()
#     return redirect('itins_detail', itin_id=itin_id)

#   return render(request,'itins/add_stop.html', {
#   'form': form,
#   'eras' : eras
#   })

@login_required
def add_stop(request, itinerary_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    eras = Era.objects.all()
    destination_id = request.GET.get('destination_id')

    if request.method == 'POST':
        form = AddStopForm(request.POST)
        if form.is_valid():
            stop = form.save(commit=False)
            stop.itinerary = itinerary
            selected_destination_id = request.POST.get('destination')  # Get the selected destination ID
            selected_destination = Destination.objects.get(id=selected_destination_id)
            stop.destination = selected_destination  # Assign the selected destination to the stop
            stop.save()
            return redirect('itins_detail', itin_id=itinerary.id)
    else:
        form = AddStopForm()

    return render(request, 'itins/add_stop.html', {'form': form, 'itinerary': itinerary, 'eras': eras, 'itinerary_id': itinerary_id})

#---------Delete Stops--------------------------------
@login_required
class delete_stop(DeleteView):
  model = Stop
  succes_url = "itins/"



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
  return render(request, 'destinations/index.html', {
    'era': era,
  })

def destinations_detail(request, era_id, dest_id):
  era = Era.objects.get(id=era_id)
  destination = Destination.objects.get(id=dest_id)

  return render(request, 'destinations/detail.html', {
    'era': era, 
    'destination': destination,
  })

# --------Add photo function (when/if we decide to have it done) (/dests/)---------------- 

# @login_required
# def add_photo(request, destination_id):
#   # photo-file maps to the "name" attr on the <input>
#   photo_file = request.FILES.get('photo-file', None)
#   if photo_file:
#     s3 = boto3.client('s3')
#     # Need a unique "key" (filename)
#     # It needs to keep the same file extension
#     # of the file that was uploaded (.png, .jpeg, etc.)
#     key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#     try:
#       bucket = os.environ['S3_BUCKET']
#       s3.upload_fileobj(photo_file, bucket, key)
#       url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
#       Photo.objects.create(url=url, destination_id=destination_id)
#     except Exception as e:
#       print('An error occurred uploading file to S3')
#       print(e)
#   return redirect('dest_detail', destination_id=destination_id)