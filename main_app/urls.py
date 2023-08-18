from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Itineraries (/itins/)

    # user -  /accounts
    path('accounts/signup/', views.signup, name='signup'),
]

