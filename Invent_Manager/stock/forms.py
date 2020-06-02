from django.forms import ModelForm
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
