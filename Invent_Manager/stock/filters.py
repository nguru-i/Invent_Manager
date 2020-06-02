import django_filters
from .models import *


class LoanFilter(django_filters.FilterSet):
    class Meta:
        model = Loan
        fields = '__all__'


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['date_created', 'price']
