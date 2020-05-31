from django.forms import ModelForm
from .models import *

class ChassisForm(ModelForm):
    class Meta:
        model = Chassis
        fields = '__all__'