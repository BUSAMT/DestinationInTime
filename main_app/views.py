# the following imports are for AWS, linked to the photo icebox feature
# import os
# import uuid
# import boto3
from django.shortcuts import get_object_or_404, render, redirect
# CBVs
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Models
from .models import Destination, Itinerary, Stop, Era

# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

# Import the login_required decorator
from django.contrib.auth.decorators import login_required

# Custom form imports
from .forms import AddStopForm, ItinCreateForm

# ------Home page view (Eras) (/home/)---------------
def home (request):
    eras = Era.objects.all().order_by('id')
    return render(request, 'home.html', {
       'eras': eras,
    })

# ------Itineraries (/itins/)-------------------------------------------
# Itineraries index
@login_required 
def itins_index(request):
  # Itins for logged in user
  itins = Itinerary.objects.filter(user=request.user).order_by('init_travel_date')
  return render(request, 'itins/index.html', {
    'itins': itins
  })


# Itinerary Details
@login_required 
def itins_detail(request, itin_id):
    itinerary = get_object_or_404(Itinerary, id=itin_id) 
    stops = itinerary.Itinerary_plan.all().order_by('init_date_at_dest')  # Retrieve all stops associated with this itinerary
    return render(request, 'itins/detail.html', {'itinerary': itinerary, 'stops': stops})


# Create Itinerary
class ItinCreate(LoginRequiredMixin, CreateView):
    model = Itinerary
    form_class = ItinCreateForm 
    # custom form overriding django one

  #overriding CBV properties to assign a user to a itinerary 
    def form_valid(self, form):
      # form.instance is the unsaved itin object / self.request.user is the logged in user object
      form.instance.user = self.request.user
      return super().form_valid(form)


# Update Itinerary
class ItinUpdate(LoginRequiredMixin, UpdateView):
    model = Itinerary
    form_class = ItinCreateForm 

    def form_valid(self, form):
        return super().form_valid(form)


# Delete Itinerary
class ItinDelete(LoginRequiredMixin, DeleteView):
  model = Itinerary
  success_url = '/itins'

# ------Stops (/itins/)----------------------------------------------- 
# Create/add one Stop associated the itinerary
@login_required
def add_stop(request, era_id, dest_id):
    destination = Destination.objects.get(id=dest_id,)
    itins = Itinerary.objects.filter(user=request.user)

    if request.method == 'POST':
        form = AddStopForm(request.POST)
        if form.is_valid():
            stop = form.save(commit=False)
            stop.destination = destination
            selected_itinerary_id = request.POST.get('itinerary')  # Get the selected itin ID
            selected_itinerary = Itinerary.objects.get(id=selected_itinerary_id)
            stop.itinerary = selected_itinerary  # Assign the selected destination to the stop
            stop.save()
            return redirect('dest_detail', era_id=era_id, dest_id=dest_id )
    else:
        form = AddStopForm()

    return render(request, 'itins/add_stop.html', {
       'form': form, 
       'destination_id': dest_id,
       'itins' : itins
         })


#Delete One Stop
@login_required
def delete_stop(request, itinerary_id, stop_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    stop = Stop.objects.get(id=stop_id)

    if request.method == 'POST':
        stop.delete()
        return redirect('itins_detail', itin_id=itinerary_id)

    return render(request, 'itins/delete_stop.html', {'itinerary': itinerary, 'stop': stop})

#Edit One Stop
@login_required
def edit_stop(request, itinerary_id, stop_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    stop = Stop.objects.get(id=stop_id)

    if request.method == 'POST':
        form = AddStopForm(request.POST, instance=stop)
        if form.is_valid():
            form.save()
            return redirect('itins_detail', itin_id=itinerary_id)
    else:
        form = AddStopForm(instance=stop)

    return render(request, 'itins/edit_stop.html', {'form': form, 'itinerary': itinerary, 'stop': stop})



#---------User------------------------------------------------------------------
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


# --------Destination (/dests/)------------------------------------------ 
# Destinations Index
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

# --------Add photo function  - Wish list icebox(/dests/)---------------- 

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