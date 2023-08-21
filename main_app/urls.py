from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.home, name='home'),
    # ------Itineraries (/itins/)---------  
    path('itins/', views.itins_index, name='itins_index'),
    path('itins/<int:itin_id>/', views.itins_detail, name='itins_detail'),
    path('itins/create/', views.ItinCreate.as_view(), name='itins_create'),
    path('itins/<int:pk>/update/', views.ItinUpdate.as_view(), name='itins_update'),
    path('itins/<int:pk>/delete/', views.ItinDelete.as_view(), name='itins_delete'),
# path to head directly to the admin site.
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    
    

    # user sign up -  /accounts
    path('accounts/signup/', views.signup, name='signup'),

    # ------Destinations (/dests/)--------- 
    path('<int:era_id>/', views.destinations_index, name='dest_index'),
]

