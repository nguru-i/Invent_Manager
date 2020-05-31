from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    contact_agent_name = models.CharField(max_length=100, default='', blank=True)
    contact_agent_email = models.EmailField(max_length=60, default='', blank=True)

    def __str__(self):
        return self.name


class ComponentInfo(models.Model):
    supplier = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING)
    item_description = models.TextField(default='')
    part_number = models.CharField(max_length=30)
    part_model = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    item_type = models.CharField(max_length=50)
    stock_quantity = models.IntegerField(default=0)
    date_received = models.DateField(default=timezone.now)
    item_location = models.CharField(max_length=50)
    tested_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    notes = models.TextField(default='')

    def __str__(self):
        return f'{self.supplier} {self.item_description}'

    class Meta:
        abstract = True



class Motherboard(ComponentInfo):
    MOTHERBOARD_TYPE = (
        ('Micro-ATX','Micro-ATX'),
        ('Mini-ATX', 'Mini-ATX'),
        ('ATX', 'ATX'),
        ('Mini-ITX', 'Mini-ITX'),
        ('TPM', 'TPM Module')
    )

    item_type = models.CharField(max_length=30, choices=MOTHERBOARD_TYPE)


class CPU(ComponentInfo):
    speed = models.DecimalField(max_digits=3, decimal_places=2)


class Memory(ComponentInfo):
    MEMORY_TYPE = (
        ('DIMM', 'DIMMM'),
        ('SODIMM', 'SODIMM'),
        ('M.2', 'M.2')
    )
    size = models.CharField(max_length=4)
    item_type = models.CharField(max_length=6, choices=MEMORY_TYPE)


class Hard_Drive(ComponentInfo):
    HARD_DRIVE_TYPE = (
        ('SSD', 'Solid State Drive'),
        ('M.2', 'M.2'),
        ('HDD', 'Mechanical Drive')
    )
    size = models.CharField(max_length=4)
    item_type = models.CharField(max_length=6, choices=HARD_DRIVE_TYPE)


class PSU(ComponentInfo):
    PSU_TYPE = (
        ('IFX', 'IFX'),
        ('DC', 'DC Adapter'),
        ('ATX', 'ATX'),

    )
    item_type = models.CharField(max_length=3, choices=PSU_TYPE)



class GPU(ComponentInfo):
    GPU_TYPE = (
        ('LP', 'Low Profile'),
        ('FH', 'Full Height'),
        ('HH', 'Half Height'),
    )
    size = models.CharField(max_length=4)
    item_type = models.CharField(max_length=3, choices=GPU_TYPE)


class Chassis(ComponentInfo):
    CHASSIS_TYPE = (
        ('FT', 'Full Tower'),
        ('AIO', 'All In One'),
        ('Mini-PC', 'Mini-PC'),
        ('2u', '2U'),

    )
    item_type = models.CharField(max_length=10, choices=CHASSIS_TYPE)

    class Meta:
        verbose_name_plural = "chassis"


class Monitor(ComponentInfo):
    MONITOR_TYPE = (
        ('LCD', 'LCD'),
        ('LED', 'LED'),
    )
    size = models.CharField(max_length=4)
    item_type = models.CharField(max_length=6, choices=MONITOR_TYPE)