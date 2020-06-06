from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['quantity']



class LoanForm(ModelForm):

    class Meta:
        model = Loan
        fields = '__all__'
        


class UserRegistrationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class UpdateLoanStatusForm(ModelForm):
    model = Loan
    fields = ['status']
