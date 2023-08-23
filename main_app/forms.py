from django.forms import ModelForm, ModelChoiceField, DateInput
from .models import Stop, Itinerary

class AddStopForm(ModelForm):
  class Meta:
    model = Stop
    # may need to revisit to add era/dest field
    fields = ['dest_name', 'dest_description','init_date_at_dest', 'end_date_at_dest', 'comments']
    widgets = {
        'init_date_at_dest': DateInput(attrs={'type': 'date'}),
        'end_date_at_dest': DateInput(attrs={'type': 'date'}),
    }
    input_formats = [
        '%Y-%m-%d',  # Year-Month-Day (e.g., 2023-08-25)
        '%d/%m/%Y',  # Day/Month/Year (e.g., 25/08/2023)
            # Add more formats as needed
        ]
    
class ItinCreateForm(ModelForm):
    class Meta:
        model = Itinerary
        fields = ['init_name', 'itin_description', 'init_travel_date', 'end_travel_date', 'user_budget']
        widgets = {
            'init_travel_date': DateInput(attrs={'type': 'date'}),
            'end_travel_date': DateInput(attrs={'type': 'date'}),
        }
    input_formats = [
        '%Y-%m-%d',  # Year-Month-Day (e.g., 2023-08-25)
        '%d/%m/%Y',  # Day/Month/Year (e.g., 25/08/2023)
            # Add more formats as needed
        ]
    
    