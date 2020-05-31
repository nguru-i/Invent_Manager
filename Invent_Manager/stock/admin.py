from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from .models import CPU, Chassis, PSU, GPU, Manufacturer

# Register your models here.

# class ChassisAdmin(admin.ModelAdmin):
#     fields = (
# 'supplier',
#     'item_description',
#     'part_number',
#     'part_model',
#     'serial_number',
#     'item_type',
#     'stock_quantity',
#     'date_received' ,
#     'item_location' ,
#     'tested_by',
# 'notes'
#     )

# admin.site.register(CPU)
# admin.site.register(Chassis, ChassisAdmin)
# admin.site.register( PSU)
# admin.site.register(GPU)
# admin.site.register(Manufacturer)

app_models = apps.get_app_config('stock').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass