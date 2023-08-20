from django.shortcuts import render, redirect
# CBVs
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

 
# AB - home view
def home (request):
    return render(request, 'home.html')

# ------Itineraries (/itins/)--------------- 
# createView
class ItinCreate(ListView):
    pass

# Itins_index
# testing out CBVs for this instead of function like catcollector - tbc
# Listview
class ItinList(DetailView):
    pass

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

