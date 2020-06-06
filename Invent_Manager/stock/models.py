from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Supplier(models.Model):
    name = models.CharField(max_length=50)
    contact_agent_name = models.CharField(
        max_length=100, default='', blank=True)
    contact_agent_email = models.EmailField(
        max_length=60, default='', blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name



class Stock(models.Model):
    
    supplier = models.ForeignKey(
        Supplier, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(blank=True)
    last_update = models.DateField('stock last updated on')
    ordered_on = models.DateField('Restock item ordered on', auto_now_add=True)
    arrives_on = models.DateField('item expected on', null=True, blank=True)

    def __str__(self):
        return self.product.name

    def was_stocked_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.last_update <= now

    was_stocked_recently.admin_order_field = 'last_update'
    was_stocked_recently.boolean = True
    was_stocked_recently.short_description = 'Stocked recently?'

    def __str__(self):
        return f'{self.quantity} {self.product.name} from {self.supplier.name}'

    def has_arrived(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.arrives_on <= now

    has_arrived.admin_order_field = 'arrives_on'
    has_arrived.boolean = True
    has_arrived.short_description = 'Supply upto date?'


# class Product(models.Model):
#     CATEGORY = (
#         ('Motherboard', 'Motherboard'),
#         ('CPU', 'CPU'),
#         ('Memory', 'Memory'),
#         ('Hard_Drive', 'Hard Drive'),
#         ('PSU', 'Power Supply Unit'),
#         ('GPU', 'Graphics Card'),
#         ('Chassis', 'Chassis'),
#         ('Monitor', 'Monitor'),
#     )

#     name = models.CharField(max_length=200, null=True)
#     price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
#     category = models.CharField(
#         max_length=200, null=True, choices=CATEGORY)
#     description = models.TextField(null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     # stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.name


class Product(models.Model):
    CATEGORY = (
        ('Motherboard', 'Motherboard'),
        ('CPU', 'CPU'),
        ('Memory', 'Memory'),
        ('Hard_Drive', 'Hard Drive'),
        ('PSU', 'Power Supply Unit'),
        ('GPU', 'Graphics Card'),
        ('Chassis', 'Chassis'),
        ('Monitor', 'Monitor'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=200, null=True, choices=CATEGORY)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    supplier = models.ForeignKey(
        Supplier, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(blank=True)
    # stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    STATUS = (
        ('Out on loan', 'Out on loan'),
        ('Returned', 'Returned')
    )
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,  null=True, on_delete=models.SET_NULL)
    loaned_on = models.DateField('item sent out on', auto_now_add=True)
    due_back = models.DateField('item due back on',null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ['due_back']

