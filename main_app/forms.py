from django.forms import ModelForm
from .models import Stop 

class StopForm(ModelForm):
  class Meta:
    model = Stop
    # may need to revisit to add era/dest field
    fields = [ 
              'dest_description', 
              'init_date_at_dest',
              'end_date_at_dest',
              'comments'  
    ]