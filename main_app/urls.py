from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView


urlpatterns = [
    #------ Home Page (eras/)-------------------------------------------
    path('', views.home, name='home'),

    # ------Itineraries (/itins/)----------------------------------------  
    path('itins/', views.itins_index, name='itins_index'),
    path('itins/<int:itin_id>/', views.itins_detail, name='itins_detail'),
    path('itins/create/', views.ItinCreate.as_view(), name='itins_create'),
    path('itins/<int:pk>/update/', views.ItinUpdate.as_view(), name='itins_update'),
    path('itins/<int:pk>/delete/', views.ItinDelete.as_view(), name='itins_delete'),

    # ------Destinations (/dests/)------------------------------------------
    # index page for destinations (aka detail page for an era)
    path('eras/<int:era_id>/', views.destinations_index, name='dest_index'),
    # details page for destination
    path('eras/<int:era_id>/destination/<int:dest_id>', views.destinations_detail, name="dest_detail"),

    # ------Stops (/itins/)------------------------------------------------  
    path('eras/<int:era_id>/destination/<int:dest_id>/addstop/', views.add_stop, name='add_stop'),
    

     # ------Delete and Edit Stops (/itins/)-----------------------------  
    path('itins/<int:itinerary_id>/edit/<int:stop_id>/', views.edit_stop, name='edit_stop'),
    path('itins/<int:itinerary_id>/delete/<int:stop_id>/', views.delete_stop, name='delete_stop'),

    #--------- Path to head directly to the admin site-------------
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),

    #----------- User sign up (/accounts/)---------------------------------
    path('accounts/signup/', views.signup, name='signup')

    

]

