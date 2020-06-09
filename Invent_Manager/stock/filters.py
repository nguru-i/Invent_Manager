import django_filters
from .models import *


class LoanFilter(django_filters.FilterSet):
    class Meta:
        model = Loan
        fields = '__all__'
        exclude = ['loaned_on','customer']


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['date_created', 'price']

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ['name']


# class StockFilter(django_filters.FilterSet):
#     class Meta:
#         model = Stock
#         fields = '__all__'
#         exclude = ['ordered_on', 'quantity']
