from django.shortcuts import render

# Create your views here.

# AB - home view
def home (request):
    return render(request, 'home.html')