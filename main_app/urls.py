from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # ------Itineraries (/itins/)---------  
    # used ListView instead of function - tbc fot itins_index
    path('itins/', views.ItinList.as_view(), name='itins_index'),
    path('itins/create/', views.ItinCreate.as_view(), name='itins_create'),
    # user sign up -  /accounts
    path('accounts/signup/', views.signup, name='signup'),
    # ------Destinations (/dests/)---------  
]

