from django.forms import ModelForm, ModelChoiceField, DateInput
from .models import Stop 

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