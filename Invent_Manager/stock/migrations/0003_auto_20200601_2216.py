# Generated by Django 3.0.3 on 2020-06-01 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_delete_supplying'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loan',
            options={'ordering': ['-loaned_on']},
        ),
    ]