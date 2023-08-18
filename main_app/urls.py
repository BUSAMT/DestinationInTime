from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # user -  /accounts
    path('accounts/', include('django.contrib.auth.urls')),
]

